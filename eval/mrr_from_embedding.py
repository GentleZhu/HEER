#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 12:39:34 2018

@author: Fang Guo
"""
import numpy as np
import argparse
import time
import warnings

def calculate_rr(batch):
    target=batch[0]
    l=batch
    l.sort(reverse=True)
    rank=l.index(target)+1
    rr=1/rank
    return rr

if __name__ == '__main__':
    start_time = time.time()
    parser = argparse.ArgumentParser(description="Read in input and output filenames.")
    
    parser.add_argument("--input-embedding", nargs="?", help="Input embedding filename.", type=str)
   
    parser.add_argument("--input-record", nargs="?", help="Input record filename.", type=str)
    
    parser.add_argument("--sample-number", nargs="?", help="Input sample number generated per node", type=int)
    
    args = parser.parse_args()
    embedding_dict={}
    input_embedding=args.input_embedding
    with open(input_embedding, "r") as f_in:
        num_nodes, dim = map(int, f_in.readline().strip().split())  # first line is special
        count=0
        for line in f_in:
            line_split = line.strip().split()
            a=list(map(float, line_split[1:]))
            embedding_dict[line_split[0]] = np.asarray(a)
        assert len(embedding_dict) == num_nodes, "Number of nodes does not agree."
    print ("Embedding loading done.", num_nodes, "nodes with dim", dim, "from", input_embedding)
    input_newfile=args.input_record
    
    with open(input_newfile, "r") as f_in:
        warnings.simplefilter('always', ImportWarning)
        count=0
        total_mrr={}

        exist=False
        rd=0
        checksametype=False
        sample_number=args.sample_number
        for line in f_in:
            line_split = line.split(' ')
            key1=line_split[0]
            key2=line_split[1]
            #print(key1[0],key2[0])
            if count==0: 
                current=[]
                if key1 in embedding_dict and key2 in embedding_dict:
                    edge_type=key1[0]+key2[0]
                    #print(edge_type,'exists')
                    if edge_type==edge_type[::-1] :
                        checksametype=True
                        if edge_type not in total_mrr:
                            total_mrr[edge_type]=[]
                    else:
                        if edge_type not in total_mrr:
                            total_mrr[edge_type]=[]
                        if edge_type[::-1] not in total_mrr:
                            total_mrr[edge_type[::-1]]=[]
                    exist =True
                    target=embedding_dict[key1].dot(embedding_dict[key2])
                    current.append(target) 
                else:
                    if key1 not in embedding_dict:
                        warning_word=key1+' does not exist.'
                        warnings.warn(warning_word)
                    if key2 not in embedding_dict:
                        warning_word=key2+' does not exist.'
                        warnings.warn(warning_word)
                    #print(target)
                count+=1
            else:
                if exist:
                    if key1 in embedding_dict and key2 in embedding_dict:
                        current.append(embedding_dict[key1].dot(embedding_dict[key2])) 
                    else:
                        if key1 not in embedding_dict:
                            warning_word=key1+' does not exist.'
                            warnings.warn(warning_word)
                        if key2 not in embedding_dict:
                            warning_word=key2+' does not exist.'
                            warnings.warn(warning_word)
                if count==sample_number and checksametype==False:
                    if exist:
                        edge_type=key1[0]+key2[0]
                        #print('10-',edge_type,current)
                        rr=calculate_rr(current)
                        total_mrr[edge_type].append(rr) 
                        current=[]
                        current.append(target)
                if count==(sample_number*2):  
                    if exist: 
                        edge_type=key1[0]+key2[0]
                        #print('20-',edge_type,current)
                        rr=calculate_rr(current)
                        total_mrr[edge_type].append(rr) 
                        exist=False
                    checksametype=False
                    count=0
                    rd+=1
                    if rd % 100000 == 0:
                        elapsed_time = time.time() - start_time
                        print(rd,' batchs finished with time',elapsed_time)
                else:
                    count+=1
        total=0
        num_mrr=0
        for key in total_mrr:
            s=sum(total_mrr[key])
            l=len(total_mrr[key])
            total=total+s
            num_mrr=num_mrr+l
            if l > 0:
                print ('edge is ',key,'with avg mrr ',s/l)
        print ('total avg is', total/num_mrr)
            
 