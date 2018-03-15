#!/bin/bash

smp=$1
out_rate=$2

echo "No additional fillters applied."

python3 ../eval/edge_rec_eval_inner_prod.py --eval-file ../input_data/dblp_"$out_rate"_out_20neg_eval_fast.txt --emb-file ../intermediate_data/dblp_"$out_rate"_out_line_samples"$smp"_dim128.emb > ../output/"$out_rate"_out_"$smp"_128.txt
#python3 ../eval/edge_rec_eval_inner_prod.py --eval-file ../input_data/dblp_"$out_rate"_out_filtered_20neg_eval.txt --emb-file ../intermediate_data/dblp_"$out_rate"_out_line_samples"$smp"_dim128.emb >> ../output/out_"$smp"_128.txt
