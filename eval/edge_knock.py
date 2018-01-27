#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 13:12:43 2017

@author: Fang Guo

"""

from itertools import islice

from random import random,sample,choice
import time
import pandas as pd
import math
import argparse


# ko_dic records all the tuple that have been knocked out, format: a: {p1,p2...}; w:{p1,p2,...}

def ko_edge(tuple_list,ko_rate,a_dic,p_dic,index2type,file_1):
    size=len(tuple_list)
    ko_dic={}
    ko_index_list=sample(range(size-1),math.ceil(size*ko_rate))
    for i in ko_index_list:
        
        tuple_list[i][-1]='0'
        node1_value=tuple_list[i][0] #it must be in P type
        node2_value=tuple_list[i][1] #it will be A or P or Other
        node1_type=index2type[node1_value]
        node2_type=index2type[node2_value]
        '''For both a_dic,p_dic and o_dic, if after knocking out, the node has an empty dictionary
           then the node will be poped in the dictionary which it belongs to. 
        '''
        if (node2_type=="A"): 
            try:
                del a_dic[node2_value][node1_value]
            except KeyError:
                pass
            if bool(a_dic[node2_value])==False:
                try:
                    del a_dic[node2_value]
                except KeyError:
                    pass
            try:
                del p_dic[node1_value][node2_value]
            except KeyError:
                pass
            if bool(p_dic[node1_value])==False:
                try:
                    del p_dic[node1_value]
                except KeyError:
                    pass
        else:
            if (node2_type=="P"): 
                try:
                    del p_dic[node2_value][node1_value]
                except KeyError:
                    pass
                if bool(p_dic[node2_value])==False:
                    try:
                        del p_dic[node2_value]
                    except KeyError:
                        pass
            else:
                try:
                    del o_dic[node2_type][node2_value][node1_value]
                except KeyError:
                    pass
                if bool(o_dic[node2_type][node2_value])==False:
                    try:
                        del o_dic[node2_type][node2_value]
                    except KeyError:
                        pass
            try:
                del p_dic[node1_value][node2_value]
            except KeyError:
                pass
            if bool(p_dic[node1_value])==False:
                try:
                    del p_dic[node1_value]
                except KeyError:
                    pass
                
        if node2_value not in ko_dic:
            ko_dic[node2_value]={}
            ko_dic[node2_value][node1_value]=1
        else:
            if node1_value not in ko_dic[node2_value]:
                ko_dic[node2_value][node1_value]=1
                
    #write result from tuple_list to file1 
    print("Started writing to file1")
    elapsed_time = time.time() - start_time
    print(elapsed_time)
    file =open(file_1,'w+')
    count=0
    content=''
    for i in tuple_list:
        if i[2]!='0':
            line=index2type[i[0]]+":"+i[0]+" "+index2type[i[1]]+":"+i[1]+" "+i[2]+"\n"
            content=content+line
        else:
            count+=1
    file.write(content)
    
    file.close()
    print("finished writing to file1")

    return ko_dic,tuple_list

            
#neagtive sampling, one from ko_list with another 20 from random sampling with same nodes
def build_file(ko_dic,a_dic,p_dic,o_dic,index2type,type_dic,sample_number,file_2,buffer_size):
    p_list=list(p_dic)
    a_list=list(a_dic)
    o_list={}
    for key in o_dic:
        o_list[key]=list(o_dic[key])
    file =open(file_2,'w+')
    #for key,value in ko_dic.items():
    print("Started writing to file2")
    elapsed_time = time.time() - start_time
    print(elapsed_time)
    content=''
    rd=0
    for key,dic in ko_dic.items():   
        content_temp=[]
        for sub_key,edge in dic.items():
            temp=index2type[key]+":"+key+" "+index2type[sub_key]+":"+sub_key+" "+str(edge)+" "+index2type[key]+index2type[sub_key]+'\n'
            content_temp.append(temp)
            if (index2type[key]=="A"):
            #10 negative sampling with same author, but non-relative paper
                if key not in a_dic or sub_key not in p_dic:
                    continue
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
                #t_list=type_dic[index2type[key]]  
                #10 negative sampling with same paper and non-relative papers
                    if sub_key not in p_dic or key not in p_dic:
                        continue
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
                    if sub_key not in p_dic or key not in o_dic[node_type]:
                        continue
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
            if rd % buffer_size ==0:
                
                file.write(content)
                content=''
    file.write(content)
    file.close()
    
    print('finished writing to file2')
    return 


#islice(file, 100000)
if __name__ == '__main__':
    
    start_time = time.time()
    #build the index2name hash table
    parser = argparse.ArgumentParser(description="Read in input and output filenames.")
    parser.add_argument("--input-p2afile", nargs="?", help="Input p2a filename.", type=str)
    parser.add_argument("--input-p2ofile", nargs="?", help="Input p20 filename.", type=str)
    parser.add_argument("--input-index2name", nargs="?", help="Input index2name filename.", type=str)
    parser.add_argument("--ko-rate", nargs="?", help="Input knockout rate.", type=float)
    parser.add_argument("--sample-number", nargs="?", help="Input sample number generated per node", type=int)
    parser.add_argument("--output-file-1", nargs="?", help="Output file_1.", type=str)
    parser.add_argument("--output-file-2", nargs="?", help="Output file_2.", type=str)
    parser.add_argument("--buffer-size", nargs="?", help="Buffer Size.", type=str)

    args = parser.parse_args()
    filename0=args.input_index2name
    index2type={}
    type_dic={}
    with open(filename0,encoding="utf-8") as file:
        for line in file:
            line=line.split()
            second_part=line[1].split(".")
            itemtype=second_part[0]
            index2type[line[0]]=itemtype
            if second_part[0] not in type_dic:
                type_dic[itemtype]={}
            type_dic[itemtype][line[0]]=1
    for itemtype in type_dic:
        type_dic[itemtype]=list(type_dic[itemtype])
    print("finished index2type and type_dic")
    
    #create p hash ,a hash and tuple list from p2a
    filename1 = args.input_p2afile
    tuple_list=[]
    p_dic={}
    a_dic={} 
    with open(filename1) as file1:
        count=0
        for line in file1:
            line=line.split()
            if(line[-1]!='0'):
                tuple_list.append(line)
                #update the both the p_dic and a_dic
                if line[0] not in p_dic:
                    p_dic[line[0]]={}
                    p_dic[line[0]][line[1]]=1
                else :
                    if line[1] not in p_dic[line[0]]:
                        p_dic[line[0]][line[1]]=1
                if line[1] not in a_dic:
                    a_dic[line[1]]={}
                    a_dic[line[1]][line[0]]=1
                else:
                    if line[0] not in a_dic[line[1]]:
                        a_dic[line[1]][line[0]]=1
            count+=1
    elapsed_time = time.time() - start_time
    print(elapsed_time)
    print("finished reading p2a")
    #get more into p hash and tuple list from p2o
    filename2 = args.input_p2ofile
    o_dic={}
    with open(filename2) as file2:
        count=0
        for line in file2:
            line=line.split()
            if(line[2]!='0'):
                tuple_list.append(line)
                #update both the p_dic and o_dic
                if line[0] not in p_dic:
                    p_dic[line[0]]={}
                if line[1] not in p_dic[line[0]]:
                    p_dic[line[0]][line[1]]=line[2]
                
                node_type=index2type[line[1]]
                #Check whether its PP type   
                if node_type.lower()=='p':
                    if line[1] not in p_dic:
                        p_dic[line[1]]={}
                    if line[0] not in p_dic[line[1]]:
                        p_dic[line[1]][line[0]]=line[2]
                else:
                    if node_type not in o_dic:
                        o_dic[node_type]={}
                    if line[1] not in o_dic[node_type]:
                        o_dic[node_type][line[1]]={}
                    if line[0] not in o_dic[node_type][line[1]]:
                        o_dic[node_type][line[1]][line[0]]=1
            count+=1
    #print(o_dic)
    #print(p_dic)
    elapsed_time = time.time() - start_time
    print(elapsed_time)
    print("finished reading p2o") 

    ko_rate=args.ko_rate
    sample_number=args.sample_number
    file_1=args.output_file_1
    file_2=args.output_file_2
    ko_dic,tuple_list=ko_edge(tuple_list,ko_rate,a_dic,p_dic,index2type,file_1)
    buffer_size=args.buffer_size
    build_file(ko_dic,a_dic,p_dic,o_dic,index2type,type_dic,sample_number,file_2,buffer_size)
    elapsed_time = time.time() - start_time
    print(elapsed_time)
    
    
  
    