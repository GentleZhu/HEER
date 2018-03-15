#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 12:39:34 2018

@author: edz
"""
import numpy as np
import sys

input_embedding=sys.argv[1]
input_newfile='../input_data/dblp_0.1_out_20neg_eval.txt'

def calculate_rr(batch):
    target=batch[0]
    l=batch
    l.sort(reverse=True)
    rank=l.index(target)+1
    rr=1/rank
    return rr

if __name__ == '__main__':
    embedding_dict={}
    #input_embedding='dblp_0.1_out_line_samples1000_dim128.emb'
    with open(input_embedding, "r") as f_in:
        num_nodes, dim = map(int, f_in.readline().strip().split())  # first line is special
        count=0
        for line in f_in:
            line_split = line.strip().split()
            a=list(map(float, line_split[1:]))
            embedding_dict[line_split[0]] = np.asarray(a)
        assert len(embedding_dict) == num_nodes, "Number of nodes does not agree."
    print ("Embedding loading done.", num_nodes, "nodes with dim", dim, "from", input_embedding)
    #input_newfile='test/file2.txt'
    with open(input_newfile, "r") as f_in:
        count=0
        total_mrr={}

        exist=False
        rd=0
        checksametype=False
        for line in f_in:
            line_split = line.split(' ')
            key1=line_split[0].lower()
            key2=line_split[1].lower()
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
                    #print(target)
                count+=1
            else:
                if exist:
                    if key1 in embedding_dict and key2 in embedding_dict:
                        current.append(embedding_dict[key1].dot(embedding_dict[key2])) 
                if count==10 and checksametype==False:
                    if exist:
                        edge_type=key1[0]+key2[0]
                        #print('10-',edge_type,current)
                        rr=calculate_rr(current)
                        total_mrr[edge_type].append(rr) 
                        current=[]
                        current.append(target)
                if count==20:  
                    if exist: 
                        edge_type=key1[0]+key2[0]
                        #print('20-',edge_type,current)
                        rr=calculate_rr(current)
                        total_mrr[edge_type].append(rr) 
                        exist=False
                    checksametype=False
                    count=0
                    rd+=1
                else:
                    count+=1
        total=0
        num_mrr=0
        for key in total_mrr:
            s=sum(total_mrr[key])
            l=len(total_mrr[key])
            total=total+s
            num_mrr=num_mrr+l
            print ('edge is ',key,'with avg mrr ',s/l)
        print ('total avg is', total/num_mrr)
            
 