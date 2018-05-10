#!/bin/bash

#e.g. bash ./src/eval.sh yago_ko_0.4 0 1 -1 yago 7

time_start=$(date +"%Y%m%d_%H%M%S")

green=`tput setaf 2`
red=`tput setaf 1`
yellow=`tput setaf 3`
reset=`tput sgr0`

# input variables
network=$1  # a.k.a. graph_name; e.g., yago_ko_0.2
epoch=$2  # number of epochs
operator=$3  # operator used to compose edge embedding from node embeddings
map=$4  # mapping on top of edge embedding
more_param=$5  # more customized parameters
gpu=$6 # working gpu for prediction
dump_timer=$7 # default dump timer
aspect_number_1=$8  # must specify
aspect_number_2=$9  # must specify


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


echo ${yellow}===HEER Testing===${reset}

curr_step=0
until [  $curr_step -gt $((epoch - 1)) ]; do
	echo $curr_step

	python2 "$root_dir"/aux/merge_score_aspem_from_per_aspect_score.py "$eval_file" "$root_dir"/intermediate_data/heer_"$network"_aspect_"$aspect_number_1"_"$curr_step"_"$operator"_"$map"_"$more_param".txt "$root_dir"/intermediate_data/heer_"$network"_aspect_"$aspect_number_2"_"$curr_step"_"$operator"_"$map"_"$more_param".txt "$root_dir"/intermediate_data/heer_"$network"_aspect_"$aspect_number_1"and"$aspect_number_2"_"$curr_step"_"$operator"_"$map"_"$more_param".txt

	bash "$root_dir"/run/eval_heer_aspem.sh $network $curr_step $operator $map $more_param $time_start "$aspect_number_1"and"$aspect_number_2"  # add $time_start to gen files for plots when running 

	let " curr_step += dump_timer "
done
