#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 12:39:34 2018

@author: Fang Guo
"""
import numpy as np
import argparse
import time

def calculate_rr(batch):
    target=batch[0]
    num_less, num_grtr = 0, 0
    for s in batch:
        if s < target:
            num_less += 1
        if s > target:
            num_grtr += 1
    rr_list = map(lambda x: 1./x, range(num_grtr+1, len(batch)-num_less+1))
    # l=sorted(batch,reverse=True)
    # rank=l.index(target)+1
    rr = sum(rr_list) / (len(batch) - num_less - num_grtr)
    return rr

if __name__ == '__main__':
    start_time = time.time()
    parser = argparse.ArgumentParser(description="Read in input and output filenames.") 
    parser.add_argument("--input-embedding", nargs="?", help="Input embedding filename.", type=str)
    parser.add_argument("--input-eval-file", nargs="?", help="Input evaluation file.", type=str) 
    parser.add_argument("--sample-number", nargs="?", help="Input sample number generated per node", type=int,default=10)
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
    input_eval_file=args.input_eval_file
    
    with open(input_eval_file, "r") as f_in:
        count=0
        total_mrr={}
        exist=False
        rd=0
        sample_number=args.sample_number
        #negative_sample_number,num_positive_edges= map(int, f_in.readline().strip().split())
        #assert negative_sample_number==args.sample_number
        for idx, line in enumerate(f_in):
            line_split = line.strip().split()
            key1=line_split[0]
            key2=line_split[1]
            #print(key1[0],key2[0])
            if count==0: 
                current=[]
                if key1 in embedding_dict and key2 in embedding_dict:
                    edge_type=line_split[-1]
                    edge_type_reverse=edge_type+'-1'
                    if edge_type not in total_mrr:
                        total_mrr[edge_type]=[]
                    if edge_type_reverse not in total_mrr:
                        total_mrr[edge_type_reverse]=[]
                    exist =True
                    target=embedding_dict[key1].dot(embedding_dict[key2])
                    current.append(target) 
                else:
                    assert key1 in embedding_dict, key1+' does not exist.'
                    assert key2 in embedding_dict, key2+' does not exist.'
                    #print(target)
                count+=1
            else:
                if exist:
                    if key1 in embedding_dict and key2 in embedding_dict:
                        current.append(embedding_dict[key1].dot(embedding_dict[key2])) 
                    else:
                        assert key1 in embedding_dict, key1+' does not exist.'
                        assert key2 in embedding_dict, key2+' does not exist.'
                if count==sample_number:
                    if exist:
                        edge_type=line_split[-1]
                        #print('10-',edge_type,current)
                        rr=calculate_rr(current)
                        total_mrr[edge_type].append(rr) 
                        current=[]
                        current.append(target)
                if count==(sample_number*2):  
                    if exist: 
                        edge_type=line_split[-1]
                        #print('20-',edge_type,current)
                        rr=calculate_rr(current)
                        total_mrr[edge_type].append(rr) 
                        exist=False
                    count=0
                    rd+=1
                    if rd % 100000 == 0:
                        elapsed_time = time.time() - start_time
                        print(rd,' batchs finished with time',elapsed_time)
                else:
                    count+=1
        idx+=1
        #assert idx/(2*negative_sample_number+1) == num_positive_edges, "Number of positive edges does not agree."
        
        total=0
        num_mrr=0
        macro_mrr=0
        key_list=[]
        for key in total_mrr:
            key_list.append(key)
        key_list.sort()
        for key in key_list:
            s=sum(total_mrr[key])
            l=len(total_mrr[key])
            macro_mrr+=s/l
            total=total+s
            num_mrr=num_mrr+l
            print('edge is '+key+'with avg mrr '+str(s/l))
        print ('macro avg is', macro_mrr/len(total_mrr))
        print ('micro avg is', total/num_mrr)
            
 
