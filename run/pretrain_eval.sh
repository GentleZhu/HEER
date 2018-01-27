#!/bin/bash

smp=$1

#python3 ../eval/edge_rec_eval_inner_prod.py --eval-file ../input_data/dblp_0.1_out_20neg_eval.txt --emb-file ../intermediate_data/dblp_0.1_out_line_samples"$smp"_dim128.emb >> ../output/out_"$smp"_128.txt
python3 ../eval/edge_rec_eval_inner_prod.py --eval-file ../input_data/dblp_0.1_out_filtered_20neg_eval.txt --emb-file ../intermediate_data/dblp_0.1_out_line_samples"$smp"_dim128.emb >> ../output/out_"$smp"_128.txt
