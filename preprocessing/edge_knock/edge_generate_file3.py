#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 17:41:05 2018

@author: edz
"""


from random import random,sample,choice
import time
import math
import argparse

def ko_edge(tuple_list,a_dic,p_dic,index2type):
    size=len(tuple_list)
    pick_dic={}
    pick_index_list=sample(range(size-1),200000)
    for i in pick_index_list:
        
        tuple_list[i][-1]='0'
        node1_value=tuple_list[i][0][2:] #it must be in P type
        node2_value=tuple_list[i][1][2:] #it will be A or P or Other

        '''For both a_dic,p_dic and o_dic, if after knocking out, the node has an empty dictionary
           then the node will be poped in the dictionary which it belongs to. 
        '''
        if node2_value not in pick_dic:
            pick_dic[node2_value]={}
            pick_dic[node2_value][node1_value]=1
        else:
            if node1_value not in pick_dic[node2_value]:
                pick_dic[node2_value][node1_value]=1
                
    print('finished pick_dic')

    return pick_dic,tuple_list

def build_file(ko_dic,a_dic,p_dic,o_dic,index2type,sample_number,file_3,buffer_size):
    p_list=list(p_dic)
    a_list=list(a_dic)
    o_list={}
    for key in o_dic:
        o_list[key]=list(o_dic[key])
    file =open(file_3,'w+')
    #for key,value in ko_dic.items():
    print("Started writing to file3")
    elapsed_time = time.time() - start_time
    print(elapsed_time)
    content=''
    rd=0
    for key,dic in ko_dic.items():   
        
        for sub_key,edge in dic.items():
            content_temp=[]
            temp=index2type[key]+":"+key+" "+index2type[sub_key]+":"+sub_key+" "+str(edge)+" "+index2type[key]+index2type[sub_key]+'\n'
            content_temp.append(temp)
            if (index2type[key]=="A"):
            #10 negative sampling with same author, but non-relative paper
                count=0
                while count<sample_number:
                    random_paper=choice(p_list)  
                    while random_paper in a_dic[key]:
                        random_paper=choice(p_list)
                    temp="A:"+key+" "+index2type[random_paper]+":"+str(random_paper)+" "+"0"+" "+"AP"+'\n'
                    content_temp.append(temp)
                    count+=1
            #10 negative sampling with same paper, but random-author
                count=0        
                while count<sample_number:
                    random_author=choice(a_list)
                    while random_author in p_dic[sub_key]:
                        random_author=choice(a_list)
                    temp="P:"+sub_key+" "+"A:"+random_author+" "+"0"+" "+"PA"+'\n'
                    content_temp.append(temp)
                    count+=1
            else: 
                if index2type[key].lower()=='p':#when key is paper type
                #10 negative sampling with same paper and non-relative papers
                    count=0
                    while count<sample_number:
                        random_paper=choice(p_list)
                        while random_paper in p_dic[sub_key]:
                            random_paper=choice(p_list)
                        temp="P:"+sub_key+" "+index2type[random_paper]+":"+random_paper+" "+"0"+" "+"PP"+'\n'
                        content_temp.append(temp)
                        count+=1
                    count=0
                    while count<sample_number:
                        random_paper=choice(p_list)
                        while random_paper in p_dic[key]:
                            random_paper=choice(p_list)
                        temp=index2type[key]+":"+key+" "+"P:"+random_paper+" "+"0"+" "+index2type[key]+"P"+'\n'
                        content_temp.append(temp)
                        count+=1
                else:# when key is other types
                    node_type=index2type[key]
                    count=0
                    
                    #10 negative sampling with same paper, but non-relative same other type nodes
                    while count<sample_number:
                        random_other=choice(o_list[node_type])
                        while random_other in p_dic[sub_key]:
                            random_other=choice(o_list[node_type])
                        temp="P:"+sub_key+" "+node_type+":"+random_other+" "+"0"+" "+"P"+node_type+'\n'
                        content_temp.append(temp)
                        count+=1
                    #10 negative sampling with same other type nodes, but non-realtive papers
                    count=0
                    while count<sample_number:
                        random_paper=choice(p_list)
                        while random_paper in o_dic[node_type][key]:
                            random_paper=choice(p_list)
                        temp=node_type+":"+key+" "+"P:"+random_paper+" "+"0"+" "+node_type+"P"+'\n'
                        content_temp.append(temp)
                        count+=1
            content=content+"".join(content_temp)
            rd+=1
        if rd % buffer_size ==0:
            print (rd,'batches finished')
            file.write(content)
            content=''
    print(rd)
    file.write(content)
    file.close()
    
    print('finished writing to file3')
    return 

if __name__ == '__main__':
    
    start_time = time.time()
    parser = argparse.ArgumentParser(description="Read in input and output filenames.")
    parser.add_argument("--input-file1", nargs="?", help="Input p2a filename.", type=str)
    parser.add_argument("--input-index2name", nargs="?", help="Input index2name filename.", type=str)
    parser.add_argument("--sample-number", nargs="?", help="Input sample number generated per node", type=int)
    parser.add_argument("--output-file-3", nargs="?", help="Output file_2.", type=str)
    parser.add_argument("--buffer-size", nargs="?", help="Buffer Size.", type=int,default=100000)
    
    args = parser.parse_args()
    filename0=args.input_index2name
    index2type={}
    with open(filename0,encoding="utf-8") as file:
        for line in file:
            line=line.split()
            second_part=line[1].split(".")
            itemtype=second_part[0]
            index2type[line[0]]=itemtype
    print('finished index2type')
    tuple_list=[]
    p_dic={}
    a_dic={} 
    o_dic={}
    filename1=args.input_file1
    count=0
    with open(filename1,encoding="utf-8") as file:
        for line in file:
            line=line.strip().split()
            node_1=line[0]
            node_2=line[1]
            node_1_type=node_1[0]
            node_1_value=node_1[2:]
            node_2_type=node_2[0]
            node_2_value=node_2[2:]
            tuple_list.append(line)
            if node_1_value not in p_dic:
                    p_dic[node_1_value]={}
            if node_2_value not in p_dic[node_1_value]:
                    p_dic[node_1_value][node_2_value]=1
            if node_2_type=='P':
                if node_2_value not in p_dic:
                    p_dic[node_2_value]={}
                if node_2_value not in p_dic[node_1_value]:
                    p_dic[node_1_value][node_2_value]=1
            if node_2_type=='A':
                if node_2_value not in a_dic:
                    a_dic[node_2_value]={}
                if node_1_value not in a_dic[node_2_value]:
                    a_dic[node_2_value][node_1_value]=1
            else:
                if node_2_type not in o_dic:
                    o_dic[node_2_type]={}
                if node_2_value not in o_dic[node_2_type]:
                    o_dic[node_2_type][node_2_value]={}
                if node_1_value not in o_dic[node_2_type][node_2_value]:
                    o_dic[node_2_type][node_2_value][node_1_value]=1
            count+=1
        print('finished reading from file_1')
        
    sample_number=args.sample_number
    file_3=args.output_file_3
    pick_dic,tuple_list=ko_edge(tuple_list,a_dic,p_dic,index2type)
    buffer_size=args.buffer_size
    build_file(pick_dic,a_dic,p_dic,o_dic,index2type,sample_number,file_3,buffer_size)
    elapsed_time = time.time() - start_time
    print(elapsed_time)

        
                
            
            
            

            
            