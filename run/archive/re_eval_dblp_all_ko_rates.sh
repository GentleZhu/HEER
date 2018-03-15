#!/bin/bash

for smp in 5000 10000 20000 50000 100000 200000
do
for i  in 0.2 0.4 0.6 0.8
do
        python3 ../eval/mrr_from_embedding.py --input-record ../input_data/dblp_"$i"_out_20neg_eval_fast.txt --input-embedding ../intermediate_data/dblp_"$i"_out_line_samples"$smp"_alpha0.1_dim128.emb --sample-number 10 > ../output/dblp_"$i"_out_pretrain_"$smp"_128.txt &
done
done
wait
