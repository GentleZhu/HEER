#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 12:39:34 2018

@author: Fang Guo
"""
import numpy as np
import sys
import time
import argparse
import warnings


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
    parser.add_argument("--input-score-file", nargs="?", help="Input score filename.", type=str)
    parser.add_argument("--input-eval-file", nargs="?", help="Input evaluaiton file.", type=str)
    parser.add_argument("--sample-number", nargs="?", help="Input sample number generated per node", type=int,default=10)

    args = parser.parse_args()
    score_dict={}
    input_scorefile=args.input_score_file
    with open(input_scorefile, "r") as f_in:
        negative_sample_number,num_positive_edges= map(int, f_in.readline().strip().split())
        for idx,line in enumerate(f_in):
            line_split = line.strip().split()
            key=line_split[0]+' '+line_split[1]
            score_dict[key]=float(line_split[2])
        print('here')
        print(idx, num_positive_edges)
        idx+=1
        assert idx/(2*negative_sample_number+1) == num_positive_edges, str(idx)+" "+str(num_positive_edges)
    print ("Loading done.", len(score_dict), "pairs from", input_scorefile)
    input_eval_file=args.input_eval_file
    
    with open(input_eval_file, "r") as f_in:
        warnings.simplefilter('always', ImportWarning)
        count=0
        total_mrr={}
        exist=False
        checksametype=False
        sample_number=args.sample_number
        rd=0
        negative_sample_number,num_positive_edges= map(int, f_in.readline().strip().split())
        assert negative_sample_number==args.sample_number
        for idx, line in enumerate(f_in):
            line_split = line.strip().split()
            key1=line_split[0]
            key2=line_split[1]
            key=key1+' '+key2
            if count==0: 
                current=[]
                if key in score_dict:
                    edge_type=line_split[-1]
                    edge_type_reverse=edge_type+'-1'
                    if edge_type not in total_mrr:
                        total_mrr[edge_type]=[]
                    if edge_type_reverse not in total_mrr:
                        total_mrr[edge_type_reverse ]=[]
                    exist=True
                    target=score_dict[key]
                    current.append(float(target) )
                    #print(target)
                else:
                    warning_word=key+" does not exist."
                    warnings.warn(warning_word)
                count+=1
            else:
                if exist:
                    if key in score_dict:
                        current.append(float(score_dict[key]) )
                    else:
                        warning_word=key+" does not exist."
                        warnings.warn(warning_word)
                if count==sample_number:
                    if exist:
                        edge_type=line_split[-1]
                        rr=calculate_rr(current)
                        total_mrr[edge_type].append(rr) 
                        current=[]
                        current.append(float(target))
                if count==(sample_number*2):  
                    if exist: 
                        edge_type=line_split[-1]
                        rr=calculate_rr(current)
                        total_mrr[edge_type].append(rr) 
                        exist=False
                    #checksametype=False
                    count=0
                    
                    rd+=1
                    if rd % 100000 == 0:
                        elapsed_time = time.time() - start_time
                        print(rd,' batchs finished with time',elapsed_time)
                else:
                    count+=1
        idx+=1
        assert idx/(2*negative_sample_number+1) == num_positive_edges, "Number of positive edges does not agree."
            
        total=0
        num_mrr=0
        macro_mrr=0
        for key in total_mrr:
            s=sum(total_mrr[key])
            l=len(total_mrr[key])
            macro_mrr+=s/l
            total=total+s
            num_mrr=num_mrr+l
            print ('edge is ',key,'with avg mrr ',s/l)
        print ('macro avg is', macro_mrr/len(total_mrr))
        print ('micro avg is', total/num_mrr)
        
        
        
 
