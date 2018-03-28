#!/bin/bash

#e.g. bash ./src/eval.sh yago_ko_0.4 0 1 -1 yago 7


green=`tput setaf 2`
red=`tput setaf 1`
yellow=`tput setaf 3`
reset=`tput sgr0`

# input variables
network=$1  # a.k.a. graph_name; e.g., yago_ko_0.2
epoch=$2  # number of epochs
operator=$3  # operator used to compose edge embedding from node embeddings
map=$4  # mapping on top of edge embedding
config=$5  # network configuration
gpu=$6 # working gpu for prediction

# find relative root directory
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
script_dir="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
root_dir="$( dirname $script_dir )"


fast_eval_file="$root_dir"/input_data/"$network"_eval_fast.txt
if [ -f "$fast_eval_file" ]; then
	eval_file="$fast_eval_file"
	fast=1
else
	echo "File $fast_eval_file does not exist. Using non-fast version for evaluation."
	eval_file="$root_dir"/input_data/"$network"_eval.txt
	fast=0
fi
eval_file="$root_dir"/input_data/"$network"_eval.txt


echo ${yellow}===HEER Testing===${reset}
python2 ./aux/separate_edges_by_types.py --input-file=$eval_file --output-dir="$root_dir"/intermediate_data/


timestamp=0
until [  $timestamp -gt $((epoch - 1)) ]; do
	echo $timestamp
	python ./src/pred.py --iter=$timestamp --batch-size=128 --dimensions=128  --graph-name=$network --data-dir="$root_dir"/intermediate_data/ --model-dir="$root_dir"/model/ \
	--pre-train-path="$root_dir"/intermediate_data/pretrained_"$network".emb --config="$root_dir"/input_data/"$config".config \
	--map_func=$map --gpu=$gpu --op=$operator --test-dir="$root_dir"/intermediate_data/ --fast=$fast >> test.log

	python2 ./aux/merge_edges_with_all_types.py --input-ref-file $eval_file --input-score-dir "$root_dir"/intermediate_data/ --input-score-keywords "$network"_pred --output-file "$root_dir"/intermediate_data/heer_"$network"_"$timestamp"_"$operator"_"$map".txt
	bash ./run/eval_heer.sh $network $timestamp $operator $map
	
	let timestamp=timestamp+2
done

