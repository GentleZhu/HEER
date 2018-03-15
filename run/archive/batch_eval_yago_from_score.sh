#!/bin/bash

score_file_dir=$1
score_file_keyword=$2
eval_file=$3

time_start=$(date +"%Y%m%d_%H%M%S")

mkdir -p ../output/

for score_file in "$score_file_dir"/*"$score_file_keyword"*
do
(
	file_basename=`basename $score_file`
	python3 ../eval/yago_mrr_from_score.py --input-score-file $score_file --input-record-file $eval_file --sample-number 10  > ../output/out_"$file_basename"
) &
done
wait
