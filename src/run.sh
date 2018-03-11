#!/bin/bash

#e.g. bash ./src/run.sh yago_ko_0.4 0 1 -1 yago 7

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

DATA_DIR=/shared/data/qiz3/data/
MODEL_DIR=/shared/data/qiz3/data/model/
#GRAPH_NAME=yago_0.4_out_
GRAPH_NAME=dblp_0.4_out_
SUFFIX=_input.p

echo ${green}===Constructing Training Net===${reset}
if [ ! -e  "$root_dir"/intermediate_data/"$network$SUFFIX" ]; then
	#python main.py --input=/shared/data/yushi2/edge_rep_codes/input_data/yago_no_gender_0.4_out.net --build-graph=True --graph-name=$GRAPH_NAME --data-dir=$DATA_DIR
	python ./src/main.py --input="$root_dir"/input_data/"$network".hin --build-graph=True \
		--graph-name=$network --data-dir="$root_dir"/intermediate_data/ --config="$root_dir"/input_data/"$config".config
fi
echo ${red}===HEER Training===${reset}
#python main.py --iter=21 --batch-size=128 --dimensions=128  --graph-name=$GRAPH_NAME --data-dir=$DATA_DIR --model-dir=$MODEL_DIR \
#--pre-train-path=/shared/data/yushi2/edge_rep_codes/intermediate_data/dblp_0.4_out_line_samples50000_alpha0.1_dim128.emb \
#--dump-timer=2 --map_func=$MAP_FUNC --op=$OP --gpu=1

