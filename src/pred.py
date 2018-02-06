import torch as t
import numpy as np
import cPickle
import sys
import neg
import argparse
import torch.utils.data as tdata
from tqdm import tqdm

def parse_args():
	'''
	Parses the node2vec arguments.
	'''
	parser = argparse.ArgumentParser(description="Run node2vec.")

	parser.add_argument('--gpu', nargs='?', default='0',
	                    help='Embeddings path')


	parser.add_argument('--graph-name', type=str, default='',
                    	help='prefix of dumped data')

	parser.add_argument('--node-types', type=list, default=['a', 'p', 'w', 'v', 'y', 'cp'])

	parser.add_argument('--edge-types', type=list, default=[(1,0),(1,1),(1,2),(1,3),(1,4)])

	parser.add_argument('--pred-type', type=int)

	parser.add_argument('--model-name', type=str)

	parser.add_argument('--test-dir', type=str)

	parser.add_argument('--out-dir', type=str)

	parser.add_argument('--batch-size', type=int, default=1000,
	                    help='Batch size. Default is 50.')



	return parser.parse_args()

if __name__ == '__main__':
	args = parse_args()
	arg = {'emb_size':128, 'window_size':1, 'batch_size':128, 'iter':10, 'neg_ratio':5, 'graph_name':'dblp_0.5_',
       'pre_train_path':'/shared/data/yushi2/edge_rep_codes/intermediate_data/dblp_0.5_out_line_samples200000_alpha0.1_dim128.emb',
       'node_types':['A','P','Y','W','V'], 'edge_types':[(1,0),(1,1),(1,2),(1,3),(1,4)], 'gpu':0, 'lr':2.5, 'mode':0}
	t.cuda.set_device(int(arg['gpu']))
	
	type_offset = cPickle.load(open('/shared/data/qiz3/data/' + arg['graph_name'] + 'offset.p'))
	model = neg.NEG_loss(type_offset=type_offset, node_types=arg['node_types'], edge_types=arg['edge_types'], embed_size=arg['emb_size'], pre_train_path='', graph_name=arg['graph_name'], mode=arg['mode'])
	#model.mode = 0
	model.load_state_dict(t.load('/shared/data/qiz3/data/model/' +  args.model_name +'.pt'))
	
	#print("Model Mode:", model.mode)
	pred_types = [0, 1, 2, 3, 4]
	suffix = '_dblp_0.5_out_20neg_eval_fast.txt'
	in_mapping = cPickle.load(open('/shared/data/qiz3/data/' + arg['graph_name'] +'in_mapping.p'))
	for idx, i in enumerate(pred_types):
		edge_prefix = []
		if arg['edge_types'][idx][0] == arg['edge_types'][idx][1]:
			edge_prefix.append(arg['node_types'][arg['edge_types'][idx][0]] + arg['node_types'][arg['edge_types'][idx][1]])
		else:
			edge_prefix += (arg['node_types'][arg['edge_types'][idx][0]] + arg['node_types'][arg['edge_types'][idx][1]],
				arg['node_types'][arg['edge_types'][idx][1]] + arg['node_types'][arg['edge_types'][idx][0]])
	#tp = int(args.pred_type)
		print("Edge Type:", i)
		print(edge_prefix)
	
	#for el in model.edge_mapping:
	#	print(el, el.weight.data.cpu().numpy().tolist())
	#sys.exit(-1)

		tp = i
	#APYWV
		for prefix in edge_prefix:
			with open(args.test_dir + prefix + suffix, 'r') as INPUT:
				_input = []
				_output = []
				for line in INPUT:
					node = line.strip().split(' ')
					_type_a, _id_a = node[0].split(':')
					_type_b, _id_b = node[1].split(':')
					#print(_type_a, _id_a)
					#if _id_a in in_mapping[_type_a] and _id_b in in_mapping[_type_b]:
					_input.append(in_mapping[_type_a][_id_a] + type_offset[_type_a])
					_output.append(in_mapping[_type_b][_id_b] + type_offset[_type_b])
					#else:
					#	continue

			input_data = tdata.TensorDataset(t.LongTensor(_input), t.LongTensor(_output))
			print(len(input_data))
			
			data_reader = tdata.DataLoader(input_data, args.batch_size, shuffle=False)
			score = []
			#model = neg.NEG_loss(type_offset=type_offset, node_types=args.node_types, edge_types=args.edge_types, embed_size=arg['emb_size'], pre_train_path=arg['pre_train'], graph_name=arg['graph_name'])
			#pbar = tqdm(total=len(data_reader) / args.batch_size)
			for i, data in enumerate(data_reader, 0):
				inputs, labels = data
				loss = model.predict(inputs, labels, tp)
				score += loss
				#pbar.update(1)
			#pbar.close()

			with open(args.test_dir + prefix + suffix, 'r') as INPUT, open(args.out_dir + prefix + suffix, 'w') as OUTPUT:
				for i, line in enumerate(INPUT):
					node = line.strip().split(' ')
					node[2] = str(score[i])
					OUTPUT.write(' '.join(node) + '\n')
			

