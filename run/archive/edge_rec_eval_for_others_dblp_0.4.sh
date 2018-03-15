#!/bin/bash

score_dir=$1  # the directory containing all score files (9 in the DBLP case) your model generates
score_keyword=$2  # the common keyword these score files have. Note that all files containing this keyword will be read in; so please make sure no other files in score_dir contains this keyword
output_keyword=$3

time_start=$(date +"%Y%m%d_%H%M%S")

mkdir -p /shared/data/qiz3/data/dblp/eval/output/

python2 /shared/data/yushi2/edge_rep_codes/aux/merge_edges_with_all_types.py --input-ref-file /shared/data/yushi2/edge_rep_codes/input_data/dblp_0.4_out_20neg_eval_fast.txt --input-score-dir $score_dir --input-score-keywords $score_keyword --output-file /shared/data/qiz3/data/dblp/eval/output/merged_score_"$output_keyword".temp
python3 /shared/data/yushi2/edge_rep_codes/eval/mrr_from_score.py --sample-number 10 --input-score-file /shared/data/qiz3/data/dblp/eval/output/merged_score_"$output_keyword".temp --input-record-file /shared/data/yushi2/edge_rep_codes/input_data/dblp_0.4_out_20neg_eval_fast.txt > /shared/data/qiz3/data/dblp/eval/result/out_"$output_keyword"_"$time_start".txt

rm /shared/data/qiz3/data/dblp/eval/output/merged_score_"$output_keyword".temp
