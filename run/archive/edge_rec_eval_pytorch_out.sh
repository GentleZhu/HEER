#!/bin/bash

score_dir=$1  # the directory containing all score files (9 in the DBLP case) your model generates
score_keyword=$2  # the common keyword these score files have. Note that all files containing this keyword will be read in; so please make sure no other files in score_dir contains this keyword
output_keyword=$3

time_start=$(date +"%Y%m%d_%H%M%S")

#python2 ../aux/merge_edges_with_all_types.py --input-ref-file ../input_data/dblp_0.1_out_20neg_eval.txt --input-score-dir $score_dir --input-score-keywords $score_keyword --output-file ../intermediate_data/merged_score.temp
#python3 ../eval/edge_rec_eval_score_provided.py --score-file ../intermediate_data/merged_score.temp --eval-file ../input_data/dblp_0.1_out_20neg_eval.txt > ../output/out_"$score_keyword"_"$time_start".txt
#python2 ../aux/merge_edges_with_all_types.py --input-ref-file ../input_data/dblp_0.1_out_filtered_20neg_eval.txt --input-score-dir $score_dir --input-score-keywords $score_keyword --output-file ../intermediate_data/merged_score.temp
#python3 ../eval/edge_rec_eval_score_provided.py --score-file ../intermediate_data/merged_score.temp --eval-file ../input_data/dblp_0.1_out_filtered_20neg_eval.txt > ../output/out_"$output_keyword"_"$time_start".txt


python2 ../aux/merge_edges_with_all_types.py --input-ref-file ../input_data/dblp_0.2_out_downsampled_20neg_eval.txt --input-score-dir $score_dir --input-score-keywords $score_keyword --output-file ../intermediate_data/merged_score_"$output_keyword".temp
python3 ../eval/edge_rec_eval_score_provided.py --score-file ../intermediate_data/merged_score_"$output_keyword".temp --eval-file ../input_data/dblp_0.2_out_downsampled_20neg_eval.txt > ../output/out_"$output_keyword"_"$time_start".txt

rm ../intermediate_data/merged_score_"$output_keyword".temp
#rm ../intermediate_data/merged_score.temp
