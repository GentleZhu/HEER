#!/bin/bash

for i in 0.4 #0.6 0.8 #0.2 0.1 0.5 #
do
    for smp in 5000 10000 
    #for smp in 100 200 500 1000 2000 5000 10000
    do
        (
        #/data/yushi2/aspect_embedding_codes/baselines/line/line -train ../input_data/yago_"$i"_out_for_line.net -output ../intermediate_data/yago_"$i"_out_line_samples"$smp"_dim128.emb -size 128 -order 1 -negative 5 -samples "$smp" -alpha 0.1 -threads 30
        python3 /shared/data/yushi2/edge_rep_codes/eval/yago_mrr_from_embedding.py --sample-number 10 --input-embedding ../intermediate_data/yago_"$i"_out_line_samples"$smp"_dim128.emb --input-record ../input_data/yago_"$i"_out_20neg_eval.txt > ../output/yago_"$i"_out_pretrain_"$smp"_128.txt
        ) &
    done
done
wait

