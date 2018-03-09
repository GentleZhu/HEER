#!/bin/bash

smp=$1
out_rate=0.2


python3 ../eval/edge_rec_eval_inner_prod.py --eval-file ../input_data/dblp_"$out_rate"_out_downsampled_20neg_eval.txt --emb-file ../intermediate_data/dblp_"$out_rate"_out_downsampled_line_samples"$smp"_dim128.emb > ../output/"$out_rate"_out_downsampled_"$smp"_128.txt

