#!/bin/bash

#e.g. bash ./src/eval.sh yago_0.4_out 0 1 2 7


green=`tput setaf 2`
red=`tput setaf 1`
yellow=`tput setaf 3`
reset=`tput sgr0`

# input variables
network=$1  # a.k.a. graph_name; e.g., yago_ko_0.2
epoch=$2  # number of epochs
operator=$3  # operator used to compose edge embedding from node embeddings
map=$4  # mapping on top of edge embedding
gpu=$5 # working gpu for prediction

# find relative root directory
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
script_dir="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
root_dir="$( dirname $script_dir )"

#EVAL_DIR=/shared/data/qiz3/data/eval/
#DATA_DIR=/shared/data/qiz3/data/
#MODEL_DIR=/shared/data/qiz3/data/model/
#GRAPH_NAME=yago_0.4_out_

echo ${yellow}===HEER Testing===${reset}
python2 ./aux/separate_edges_by_types.py --input-file="$root_dir"/input_data/"$network"_20neg_eval.txt --output-dir="$root_dir"/intermediate_data/
python ./src/pred_yago.py --iter=$epoch --batch-size=128 --dimensions=128  --graph-name=$network --data-dir="$root_dir"/intermediate_data/ --model-dir="$root_dir"/model/ \
--pre-train-path=/shared/data/yushi2/edge_rep_codes/intermediate_data/yago_no_gender_0.4_out_line_samples5000_alpha0.1_dim128.emb \
--map_func=$map --gpu=$gpu --op=$operator --test-dir="$root_dir"/intermediate_data/

python2 ./aux/merge_edges_with_all_types.py --input-ref-file "$root_dir"/input_data/"$network"_20neg_eval.txt --input-score-dir "$root_dir"/intermediate_data/ --input-score-keywords yago_no_gender_0.4_out_ --output-file "$root_dir"/intermediate_data/heer_"$network"_"$epoch"_"$operator"_"$map".txt
bash ./run/eval_heer.sh $network $epoch $operator $map
