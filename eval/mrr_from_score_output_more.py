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
    l=batch
    l.sort(reverse=True)
    rank=l.index(target)+1
    rr=1/rank
    return rr

if __name__ == '__main__':
    start_time = time.time()
    parser = argparse.ArgumentParser(description="Read in input and output filenames.")
    parser.add_argument("--input-score-file", nargs="?", help="Input score filename.", type=str)
    parser.add_argument("--input-record-file", nargs="?", help="Input record filename.", type=str)
    parser.add_argument("--sample-number", nargs="?", help="Input sample number generated per node", type=int)

    args = parser.parse_args()
    score_dict={}
    input_scorefile=args.input_score_file
    with open(input_scorefile, "r") as f_in:
        for line in f_in:
            line_split = line.strip().split()
            key=line_split[0]+' '+line_split[1]
            score_dict[key]=line_split[2]
    print ("Loading done.", len(score_dict), "pairs from", input_scorefile)
    input_recordfile=args.input_record_file
    
    with open(input_recordfile, "r") as f_in:
        warnings.simplefilter('always', ImportWarning)
        count=0
        total_mrr={}
        
        exist=False
        checksametype=False
        sample_number=args.sample_number

        rd=0
        for line in f_in:
            line_split = line.split(' ')
            key1=line_split[0]
            key2=line_split[1]
            key=key1+' '+key2
            
            #print(key1[0],key2[0])
            if count==0: 
                current=[]
                if key in score_dict:
                    edge_type=key1[0]+key2[0]
                    if edge_type==edge_type[::-1] :
                        checksametype=True
                        if edge_type not in total_mrr:
                            total_mrr[edge_type]=[]
                    else:
                        if edge_type not in total_mrr:
                            total_mrr[edge_type]=[]
                        if edge_type[::-1] not in total_mrr:
                            total_mrr[edge_type[::-1]]=[]
                    exist=True
                    target=score_dict[key]
                    current.append(float(target)) 
                    #print(target)
                else:
                    warning_word=key+" does not exist."
                    warnings.warn(warning_word)
                   
                count+=1
            else:
                if exist:
                    if key in score_dict:
                        current.append(float(score_dict[key])) 
                    else:
                        warning_word=key+" does not exist."
                        warnings.warn(warning_word)
                if count==sample_number and checksametype==False:
                    if exist:
                        edge_type=key1[0]+key2[0]
                        #print('10-',edge_type,current)
                        print(current)
                        rr=calculate_rr(current)
                        total_mrr[edge_type].append(rr) 
                        
                        current=[]
                        current.append(float(target))
                if count==(sample_number*2):  
                    if exist: 
                        edge_type=key1[0]+key2[0]
                        #print('20-',edge_type,current)
                        print(current)
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
            print (rd, "------------------------")
            if rd == 10:
                print(total_mrr)
                break
            
        total=0
        num_mrr=0
        
        for key in total_mrr:
            s=sum(total_mrr[key])
            l=len(total_mrr[key])
            total=total+s
            num_mrr=num_mrr+l
            
            print ('edge is ',key,'with avg mrr ',s/l)
        print ('total avg is', total/num_mrr)
        
 
