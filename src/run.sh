green=`tput setaf 2`
red=`tput setaf 1`
yellow=`tput setaf 3`
reset=`tput sgr0`

DATA_DIR=/shared/data/qiz3/data/
MODEL_DIR=/shared/data/qiz3/data/model/
GRAPH_NAME=yago_0.4_out_
SUFFIX=input.p

echo ${green}===Constructing Training Net===${reset}
if [ ! -e  $DATA_DIR$GRAPH_NAME$SUFFIX ]; then
	python main.py --input=/shared/data/yushi2/edge_rep_codes/input_data/yago_no_gender_0.4_out.net --build-graph=True --graph-name=$GRAPH_NAME --data-dir=$DATA_DIR
fi
echo ${red}===HEER Training===${reset}
python main.py --iter=10 --batch-size=128 --dimensions=128  --graph-name=$GRAPH_NAME --data-dir=$DATA_DIR --model-dir=$MODEL_DIR \
--pre-train-path=/shared/data/yushi2/edge_rep_codes/intermediate_data/yago_no_gender_0.4_out_line_samples5000_alpha0.1_dim128.emb \
--dump-timer=2 --map_func=2 --gpu=7
