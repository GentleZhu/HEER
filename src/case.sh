#!/bin/bash

#e.g. bash ./src/case.sh yago_ko_0.4 43 1 0 rescale_0.1_lr_10_lrr_10 input_data/0.1_46059_30292_full.hin 3 6

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

sub_net=$6
gpu=$7 # working gpu for prediction
dump_timer=${8:-2} # default dump timer


# find relative root directory
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
script_dir="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
root_dir="$( dirname $script_dir )"

echo ${yellow}===HEER Testing===${reset}

curr_step=0
until [  $curr_step -gt $((epoch - 1)) ]; do
	echo $curr_step
	python2 "$root_dir"/src/pred_case.py --iter=$curr_step --batch-size=128 --dimensions=128  --graph-name=$network --data-dir="$root_dir"/intermediate_data/ --model-dir="$root_dir"/intermediate_data/model/ \
	--pre-train-path="$root_dir"/intermediate_data/pretrained_"$network".emb --more-param="$more_param" \
	--map_func=$map --gpu=$gpu --op=$operator --test-dir="$root_dir"/intermediate_data/ --sub-net=$sub_net
	let " curr_step += dump_timer "
done