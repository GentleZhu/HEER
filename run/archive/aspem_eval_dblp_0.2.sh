#!/bin/bash

score_prefix=$1  # the directory containing all score files (9 in the DBLP case) your model generates
output_keyword=$2

time_start=$(date +"%Y%m%d_%H%M%S")

mkdir -p ../output/

python3 ../eval/edge_rec_eval_score_provided.py --score-file "$score_prefix"_pay_score.txt --eval-file /shared/data/yushi2/edge_rep_codes/input_data/dblp_0.2_out_20neg_eval_fast.txt > ../output/out_aspem_"$output_keyword"_pay_"$time_start".txt
python3 ../eval/edge_rec_eval_score_provided.py --score-file "$score_prefix"_papvw_score.txt --eval-file /shared/data/yushi2/edge_rep_codes/input_data/dblp_0.2_out_20neg_eval_fast.txt > ../output/out_aspem_"$output_keyword"_papvw_"$time_start".txt
python3 ../eval/edge_rec_eval_score_provided.py --score-file "$score_prefix"_mean_score.txt --eval-file /shared/data/yushi2/edge_rep_codes/input_data/dblp_0.2_out_20neg_eval_fast.txt > ../output/out_aspem_"$output_keyword"_mean_"$time_start".txt

