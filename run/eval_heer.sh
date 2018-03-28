#!/bin/bash

# e.g.: ./eval_heer.sh yago_ko_0.1 10 diag bn

time_start=$(date +"%Y%m%d_%H%M%S")

# find relative root directory
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
script_dir="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
root_dir="$( dirname $script_dir )"

# input variables
network=$1  # a.k.a. graph_name; e.g., yago_ko_0.2
epoch=$2  # number of epochs
operator=$3  # operator used to compose edge embedding from node embeddings
map=$4  # mapping on top of edge embedding

# optional argument specifying model evaluation start time when evaluating multiple epochs from the same model
# null if evaluating a single file
per_epoch_eval_time_start=${5:-null}

# files
score_file="$root_dir"/intermediate_data/heer_"$network"_"$epoch"_"$operator"_"$map".txt
fast_eval_file="$root_dir"/input_data/"$network"_eval_fast.txt
if [ -f "$fast_eval_file" ]; then
	eval_file="$fast_eval_file"
else
	echo "File $fast_eval_file does not exist. Using non-fast version for evaluation."
	eval_file="$root_dir"/input_data/"$network"_eval.txt
fi
output_file="$root_dir"/output/out_heer_"$network"_"$epoch"_"$operator"_"$map"_"$time_start".txt

python3 "$root_dir"/eval/mrr_from_score.py --input-score-file $score_file --input-eval-file $eval_file > "$output_file"

# when the 5th arg, per_epoch_eval_time_start, is specified, multi-epoch is called by "$root_dir"/src/eval.sh; two more files should be generated
if [ "$per_epoch_eval_time_start" != "null" ]; then
  tail -n 1 "$output_file" | awk '{print $NF}' >> "$root_dir"/output/mrr_micro_heer_"$network"_"$operator"_"$map"_"$per_epoch_eval_time_start".txt
  tail -n 2 "$output_file" | head -n 1 | awk '{print $NF}' >> "$root_dir"/output/mrr_macro_heer_"$network"_"$operator"_"$map"_"$per_epoch_eval_time_start".txt
fi
