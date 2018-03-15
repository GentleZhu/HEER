#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 21:51:01 2018

@author: edz
"""

from random import random,sample,choice
import time
import math
import argparse
import os

def ko_edge(tuple_list,ko_rate,edge_dictionary,node_type_dictionary,sample_number,file_hin,buffer_size):
    size=len(tuple_list)
    ko_dic={}
    ko_index_list=sample(range(size-1),math.ceil(size*ko_rate))
    #print(tuple_list)
    repeat_count=0
    for i in ko_index_list:
        tuple_list[i][-2]='0'
        node_1_value=tuple_list[i][0] 
        node_2_value=tuple_list[i][1] 
        node_1_type=node_type_dictionary[node_1_value]
        node_2_type=node_type_dictionary[node_2_value]
        edge_type=tuple_list[i][3]
        if node_1_value in edge_dictionary[node_1_type]:
            if node_2_value in edge_dictionary[node_1_type][node_1_value]:
                if edge_type in edge_dictionary[node_1_type][node_1_value][node_2_value]:
                    edge_dictionary[node_1_type][node_1_value][node_2_value].remove(edge_type)
                if not edge_dictionary[node_1_type][node_1_value][node_2_value]:
                    try:
                        del edge_dictionary[node_1_type][node_1_value][node_2_value]
                    except KeyError:
                        pass
            if bool(edge_dictionary[node_1_type][node_1_value])==False:
                try:
                    del edge_dictionary[node_1_type][node_1_value]
                except KeyError:
                    pass
        if node_2_value in edge_dictionary[node_2_type]:
            if node_1_value in edge_dictionary[node_2_type][node_2_value]:
                if edge_type in  edge_dictionary[node_2_type][node_2_value][node_1_value]:
                    edge_dictionary[node_2_type][node_2_value][node_1_value].remove(edge_type)
                if not edge_dictionary[node_2_type][node_2_value][node_1_value]:
                    try:
                        del edge_dictionary[node_2_type][node_2_value][node_1_value]
                    except KeyError:
                        pass
            if bool(edge_dictionary[node_2_type][node_2_value])==False:
                try:
                    del edge_dictionary[node_2_type][node_2_value]
                except KeyError:
                    pass
        #print(node_1_value,node_2_value)
        if node_1_value not in ko_dic:
            ko_dic[node_1_value]={}
            ko_dic[node_1_value][node_2_value]=[edge_type]
        else: 
            #print(node_1_value,node_2_value)
            if node_2_value not in ko_dic[node_1_value]:
                #print('11')
                ko_dic[node_1_value][node_2_value]=[edge_type]
            elif edge_type not in ko_dic[node_1_value][node_2_value]:
                #print('111')
                ko_dic[node_1_value][node_2_value].append(edge_type)
            else:
                repeat_count+=1
    #print(edge_dictionary)
    print("Started writing to hin")
    elapsed_time = time.time() - start_time
    print(elapsed_time)
    file =open(file_hin,'w+')
    content=''
    count=0
    for i in tuple_list:
        if i[2]!='0':
            line=node_type_dictionary[i[0]]+":"+i[0]+" "+node_type_dictionary[i[1]]+":"+i[1]+" "+i[2]+' '+i[3]+"\n"
            content=content+line
        count+=1
        if count % buffer_size ==0:
            print (count,'batches finished')
            file.write(content)
            content=''
    file.write(content)
    file.close()
    print("finished writing to hin")
    return edge_dictionary,ko_dic,tuple_list
    
def check_connection(ko_dic,edge_dictionary,node_1_value,node_2_type,node_2_value):
    if node_1_value in edge_dictionary[node_2_type][node_2_value] :
        return True
    else:
        if node_1_value in ko_dic:
            if node_2_value in ko_dic[node_1_value]:
                return True
        return False
    
def get_file_eval_info(ko_dic,edge_dictionary,node_type_dictionary,sample_number,file_eval,buffer_size):
    new_edge_dictionary={}
    for node_type in edge_dictionary:
        new_edge_dictionary[node_type]=list(edge_dictionary[node_type])
    not_valid_count=0
    valid_count=0
    for node_1_value,dic in ko_dic.items():
        for node_2_value,edge_list in dic.items():
            for edge in edge_list:
                node_1_type=node_type_dictionary[node_1_value]
                node_2_type=node_type_dictionary[node_2_value]
                if node_1_value not in edge_dictionary[node_1_type] or node_2_value not in edge_dictionary[node_2_type]:
                    #print(node_1_type,node_1_value,node_2_type,node_2_value)
                    not_valid_count+=1
                    continue
                valid_count+=1
                #sample_number of negative edges with same node_1, but different node_2
    file_eval_info=str(sample_number)+' '+str(valid_count)+'\n'
    return file_eval_info
    

def build_file(ko_dic,edge_dictionary,node_type_dictionary,sample_number,file_eval,buffer_size):
    new_edge_dictionary={}
    for node_type in edge_dictionary:
        new_edge_dictionary[node_type]=list(edge_dictionary[node_type])
    file =open(file_eval,'w+')
    #for key,value in ko_dic.items():
    print("Started writing to eval file")
    elapsed_time = time.time() - start_time
    print(elapsed_time)
    file_eval_info=get_file_eval_info(ko_dic,edge_dictionary,node_type_dictionary,sample_number,file_eval,buffer_size)
    file.write(file_eval_info)
    content=''
    rd=0
    not_valid_count=0
    
    for node_1_value,dic in ko_dic.items():
        for node_2_value,edge_list in dic.items():
            for edge in edge_list:
                content_temp=[]
                node_1_type=node_type_dictionary[node_1_value]
                node_2_type=node_type_dictionary[node_2_value]
                temp=node_1_type+":"+node_1_value+" "+node_2_type+":"+node_2_value+" "+'1 '+edge+'\n'
                
                if node_1_value not in edge_dictionary[node_1_type] or node_2_value not in edge_dictionary[node_2_type]:
                    #print(node_1_type,node_1_value,node_2_type,node_2_value)
                    not_valid_count+=1
                    continue
                #sample_number of negative edges with same node_1, but different node_2
                content_temp.append(temp)
                count=0
                while count<sample_number:
                    random_node_2_value=choice(new_edge_dictionary[node_2_type])
                    while (random_node_2_value in edge_dictionary[node_1_type][node_1_value] or random_node_2_value in ko_dic[node_1_value]):
                        random_node_2_value=choice(new_edge_dictionary[node_2_type])
                    temp=node_1_type+":"+node_1_value+" "+node_2_type+":"+random_node_2_value+" "+'0 '+edge+'\n'
                    content_temp.append(temp)
                    count+=1
                #sample_number of nagative edges with same node_2 but differnt node_1
                count=0
                while count<sample_number:
                    random_node_1_value=choice(new_edge_dictionary[node_1_type])
                    while check_connection(ko_dic,edge_dictionary,random_node_1_value,node_2_type,node_2_value):
                    #while (random_node_1_value in edge_dictionary[node_2_type][node_2_value] or node_2_value in ko_dic[node_1_value]):
                        random_node_1_value=choice(new_edge_dictionary[node_1_type])
                    temp=node_2_type+":"+node_2_value+" "+node_1_type+":"+random_node_1_value+" "+'0 '+edge+'-1'+'\n'
                    content_temp.append(temp)
                    count+=1  
                content=content+"".join(content_temp)
                rd+=1
                if rd % buffer_size ==0:
                    print (rd,'batches finished')
                    file.write(content)
                    content=''
    file.write(content)
    file.close()
    print('finished writing to eval file with not valid count ', not_valid_count)
def build_config(edge_full_index_list,edge_index_list,node_index_list,edge_direction_list,file_config):
    assert len(edge_full_index_list) == len(edge_index_list), "Number of edges in edge_full_index_list does not agree with edge_index_list"
    assert len(edge_index_list) == len(edge_direction_list), "Number of edges in edge_index_list does not agree with edge_direction_list"
    file =open(file_config,'w+')
    file.write(str(edge_full_index_list))
    file.write('\n')
    file.write(str(node_index_list))
    file.write('\n')
    file.write(str(edge_index_list))
    file.write('\n')
    file.write(str(edge_direction_list))
    file.close()
    print('finished config file.')
            
    
if __name__ == '__main__':
    start_time = time.time()
    #build the index2name hash table
    parser = argparse.ArgumentParser(description="Read in input and output filenames.")
    parser.add_argument("--input-hin-file", nargs="?", help="Input yago filename.", type=str)
    parser.add_argument("--ko-rate", nargs="?", help="Input knockout rate.", type=float)
    parser.add_argument("--sample-number", nargs="?", help="Input sample number generated per node", type=int,default=10)
    parser.add_argument('--data-set-name', nargs='?', help='data_set_name used to build network.', type=str,default='unknown')
    parser.add_argument('--path-output', nargs='?', help='The output to write.', type=str,default='.')
    parser.add_argument('--buffer-size', nargs='?', help='Buffer Size.', type=int, default= 500000)
    
    args = parser.parse_args()
    input_hin_file=args.input_hin_file
    edge_dictionary={}
    tuple_list=[]
    node_type_dictionary={}
    node_index_dictionary={}
    edge_index_dictionary={}
    node_index_list=[]
    edge_index_list=[]
    edge_full_index_list=[]
    edge_direction_list=[]
    print("Start reading from hin file ",input_hin_file)
     # holds lines already seen
    with open(input_hin_file,encoding="utf-8") as file:
        count=0
        node_index_count=0
        edge_index_count=0
        for line in file:
            edge_check=False
            if line not in edge_index_dictionary:
                edge_index_dictionary[line]=edge_index_count
                edge_index_list.append(str(edge_index_count))
                edge_index_count+=1
                edge_check=True
            line=line.split()
            node_1=line[0]
            node_1=node_1.split(':')
            node_1_type=node_1[0]
            node_1_value=node_1[1]
            node_2=line[1]
            node_2=node_2.split(':')
            node_2_type=node_2[0]
            node_2_value=node_2[1]
            weight=line[2]
            edge_type=line[3]
            edge_info=edge_type.split(':')
            edge_value=edge_info[0]
            edge_directed=edge_info[1]
            if node_1_value not in node_index_dictionary:
                node_index_dictionary[node_1_value]=node_index_count
                node_index_list.append(str(node_index_count))
                node_index_count+=1
            if node_2_value not in node_index_dictionary:
                node_index_dictionary[node_2_value]=node_index_count
                node_index_list.append(str(node_index_count))
                node_index_count+=1
            if edge_check:
                edge_full_index_list.append([str(node_index_dictionary[node_1_value]),str(node_index_dictionary[node_2_value])])
                if edge_directed=='u':
                    edge_direction_list.append(0)
                else:
                    edge_direction_list.append(1)
            #build the edge_dictionary, saving the edges of both nodes into dictionary 
            if node_1_type not in edge_dictionary:
                edge_dictionary[node_1_type]={}
            if node_1_value not in edge_dictionary[node_1_type]:
                edge_dictionary[node_1_type][node_1_value]={}
            if node_2_value not in edge_dictionary[node_1_type][node_1_value]:
                edge_dictionary[node_1_type][node_1_value][node_2_value]=[]
            if edge_type not in edge_dictionary[node_1_type][node_1_value][node_2_value]:
                edge_dictionary[node_1_type][node_1_value][node_2_value].append(edge_type)
            if node_2_type not in edge_dictionary:
                edge_dictionary[node_2_type]={}
            if node_2_value not in edge_dictionary[node_2_type]:
                edge_dictionary[node_2_type][node_2_value]={}
            if node_1_value not in edge_dictionary[node_2_type][node_2_value]:
                edge_dictionary[node_2_type][node_2_value][node_1_value]=[]
            if edge_type not in edge_dictionary[node_2_type][node_2_value][node_1_value]:
                edge_dictionary[node_2_type][node_2_value][node_1_value].append(edge_type)
            #build node_type_dictionary, saving each node's type
            if node_1_value not in node_type_dictionary:
                node_type_dictionary[node_1_value]=node_1_type
            if node_2_value not in node_type_dictionary:
                node_type_dictionary[node_2_value]=node_2_type
            #build tuple_list, saving each line to tuple_list
            temp=[node_1_value,node_2_value,weight,edge_type]
            tuple_list.append(temp)
            count+=1

    print('finished reading from ',input_hin_file)
    ko_rate=args.ko_rate
    sample_number=args.sample_number
    buffer_size=args.buffer_size
    data_set_name=args.data_set_name
    path_out=args.path_output
    file_config=os.path.join(path_out,data_set_name+'.config') 
    
    file_hin=os.path.join(path_out,data_set_name+'_ko_'+str(ko_rate)+'.hin')
    file_eval=os.path.join(path_out,data_set_name+'_ko_'+str(ko_rate)+'_eval.txt')
    #print(edge_dictionary)
    build_config(edge_full_index_list,edge_index_list,node_index_list,edge_direction_list,file_config)
    '''
    edge_dictionary,ko_dic,tuple_list=ko_edge(tuple_list,ko_rate,edge_dictionary,node_type_dictionary,sample_number,file_hin,buffer_size)
    build_file(ko_dic,edge_dictionary,node_type_dictionary,sample_number,file_eval,buffer_size)
    '''
    elapsed_time = time.time() - start_time
    print(elapsed_time)
            