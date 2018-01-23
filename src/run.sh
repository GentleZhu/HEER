#star schema
python main.py --input=/shared/data/qiz3/data/dblp.hin --iter=10 --batch-size=128 --dimensions=100 --gpu=1 --pre-train-path=/shared/data/qiz3/data/dim_100_attr_nodes_apvwy.emb

#general schema
#edge_rep=/shared/data/qiz3/data/

python main.py --input=/shared/data/qiz3/data/dblp_0.1_out.net --first-time=True --graph-name=dblp --node-types=APWVY