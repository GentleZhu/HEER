#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 13:12:43 2017

@author: edz
"""

from itertools import islice

from random import random,sample,choice
import time
import pandas as pd
import math



# ko_dic records all the tuple that have been knocked out, format: a: {p1,p2...}

def ko_edge(tuple_list,ko_rate,a_dic,index2type):
    size=len(tuple_list)
    ko_dic={}
    ko_index_list=sample(range(size-1),math.ceil(size*ko_rate))
    for i in ko_index_list:
        tuple_list[i][-1]='0'
    
        if tuple_list[i][1] not in ko_dic:
            ko_dic[tuple_list[i][1]]={}
            ko_dic[tuple_list[i][1]][tuple_list[i][0]]=1
        else:
            if tuple_list[i][0] not in ko_dic[tuple_list[i][1]]:
                ko_dic[tuple_list[i][1]][tuple_list[i][0]]=1
    #write result from tuple_list to file1 
    file =open('file1.txt','w')
    count=0
    for i in tuple_list:
        if i[2]!='0':
            line=index2type[i[0]]+":"+i[0]+" "+index2type[i[1]]+":"+i[1]+" "+i[2]
            file.write(line)
            file.write('\n')
        else:
            count+=1
    file.close()
    print("finished file1")
    return ko_dic,tuple_list

            
#neagtive sampling, one from ko_list with another 20 from random sampling with same author
def build_file(ko_dic,a_dic,p_dic,o_dic,index2type,type_dic):
    p_list=list(p_dic)
    a_list=list(a_dic)
    file =open('file2.txt','w')
    #for key,value in ko_dic.items():
    for key,dic in ko_dic.items():   
        
        for sub_key,edge in dic.items():
            temp=index2type[key]+":"+key+" "+index2type[sub_key]+":"+sub_key+" "+str(edge)+" "+index2type[key]+index2type[sub_key]
            file.write(temp)
            file.write('\n')
            
            if (index2type[key]=="A"):
            #10 negative sampling with same author, but non-relative paper
                count=0
                while count<50:
                    random_paper=choice(p_list)      
                    while random_paper in a_dic[key]:
                        random_paper=choice(p_list)
                    temp="A:"+key+" "+index2type[random_paper]+":"+str(random_paper)+" "+"0"+" "+"AP"
                    file.write(temp)
                    file.write('\n')
                    count+=1
            #10 negative sampling with same paper, but random-author
                count=0
                while count<50:
                    random_author=choice(a_list)
                    while sub_key in a_dic[random_author]:
                        random_author=choice(a_list)
                    temp="P:"+sub_key+" "+"A:"+random_author+" "+"0"+" "+"PA"
                    file.write(temp)
                    file.write('\n')
                    count+=1
            else:
                t_list=type_dic[index2type[key]]
                #when key is others:
                #10 negative sampling with same paper, but non-relative other
                count=0
                while count<50:
                    random_o=choice(t_list)
                    while random_o in p_dic[sub_key]:
                        random_o=choice(t_list)
                    temp="P:"+sub_key+" "+index2type[random_o]+":"+random_o+" "+"0"+" "+"P"+index2type[key]
                    file.write(temp)
                    file.write('\n')
                    count+=1
                count=0
                while count<50:
                    random_paper=choice(p_list)
                    while key in p_dic[random_paper]:
                        random_paper=choice(p_list)
                    temp=index2type[key]+":"+key+" "+"P:"+random_paper+" "+"0"+" "+index2type[key]+"P"
                    file.write(temp)
                    file.write('\n')
                    count+=1
            
    file.close()
    return 


#islice(file, 100000)
if __name__ == '__main__':
    
    start_time = time.time()
    #build the index2name hash table
    
    filename0="index2name.txt"
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
    filename1 = "all_p2a.txt"
    tuple_list=[]
    p_dic={}
    a_dic={} 
    with open(filename1) as file1:
        for line in file1:
            line=line.split()
            if(line[-1]!='0'):
                tuple_list.append(line)
                if line[0] not in p_dic:
                    p_dic[line[0]]={}
                if line[1] not in a_dic:
                    a_dic[line[1]]={}
                    a_dic[line[1]][line[0]]=1
                else:
                    if line[0] not in a_dic[line[1]]:
                        a_dic[line[1]][line[0]]=1
    
    elapsed_time = time.time() - start_time
    print(elapsed_time)
    print("finished reading p2a")
    #get more into p hash and tuple list from p2o
    filename2 = "all_p2o.txt"
    o_dic={}
    with open(filename2) as file2:
        for line in file2:
            line=line.split()
            if(line[2]!='0'):
                tuple_list.append(line)
                if line[0] not in p_dic:
                    p_dic[line[0]]={}
                if line[1] not in p_dic[line[0]]:
                    p_dic[line[0]][line[1]]=line[2]
                if line[1] not in o_dic:
                    o_dic[line[1]]=1
    #print(o_dic)
    #print(p_dic)
    elapsed_time = time.time() - start_time
    print(elapsed_time)
    print("finished reading p2o") 
    ko_rate=0.1
    ko_dic,tuple_list=ko_edge(tuple_list,ko_rate,a_dic,index2type)
    build_file(ko_dic,a_dic,p_dic,o_dic,index2type,type_dic)
    elapsed_time = time.time() - start_time
    print(elapsed_time)
    
    '''
    type_dic={}
    
    with open('file1.txt',encoding="utf-8") as file:
        count=0
        for line in file:
            line=line.split()
            part1=line[0]
            part2=line[1]
            part1=part1.split(":")
            if part1[0] not in type_dic:
                type_dic[part1[0]]={}
            if part1[1] not in type_dic[part1[0]]:
                type_dic[part1[0]][part1[1]]=1
            part2=part2.split(":")
            if part2[0] not in type_dic:
                type_dic[part2[0]]={}
            if part2[1] not in type_dic[part2[0]]:  
                type_dic[part2[0]][part2[1]]=1
    with open('file2.txt',encoding="utf-8") as file:
        for line in file:
            line=line.split()
            if line[2]=='1':
                part1=line[0]
                part2=line[1]
                part1=part1.split(":")
                if part1[0] not in type_dic:
                    type_dic[part1[0]]={}
                if part1[1] not in type_dic[part1[0]]:
                    type_dic[part1[0]][part1[1]]=1
                part2=part2.split(":")
                if part2[0] not in type_dic:
                    type_dic[part2[0]]={}
                if part2[1] not in type_dic[part2[0]]:  
                    type_dic[part2[0]][part2[1]]=1
    for ty in type_dic:
        print(ty,len(type_dic[ty]))'''
    