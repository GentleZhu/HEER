# README
## Train embedding
source /shared/data/qiz3/qiz3/bin/activate

cd /shared/data/qiz3/_Github/edgesemantics/src/

python main.py --input=/shared/data/qiz3/data/dblp.hin --iter=50 --batch-size=128 --dimensions=100 --gpu=1

PS:You may need to manually change line:55 in emb_lib.py to change settings of auto saving.

## decode model into embedding files
python decoder.py model_prefix epoch_number

PS:see decoder.py see dumped embedding path
