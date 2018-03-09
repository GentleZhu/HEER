#!/bin/bash

score_dir=$1  # the directory containing all score files (9 in the DBLP case) your model generates
score_keyword=$2  # the common keyword these score files have. Note that all files containing this keyword will be read in; so please make sure no other files in score_dir contains this keyword
output_keyword=$3

time_start=$(date +"%Y%m%d_%H%M%S")

mkdir -p ../output/

python2 /shared/data/yushi2/edge_rep_codes/aux/merge_edges_with_all_types.py --input-ref-file /shared/data/yushi2/edge_rep_codes/input_data/dblp_0.2_out_20neg_eval_fast.txt --input-score-dir $score_dir --input-score-keywords $score_keyword --output-file ../output/merged_score_"$output_keyword".temp
python3 ../eval/edge_rec_eval_score_provided.py --score-file ../output/merged_score_"$output_keyword".temp --eval-file /shared/data/yushi2/edge_rep_codes/input_data/dblp_0.2_out_20neg_eval_fast.txt > ../output/out_"$output_keyword"_"$time_start".txt

rm ../output/merged_score_"$output_keyword".temp
