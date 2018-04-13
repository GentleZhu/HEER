import torch as t
import numpy as np
import cPickle
import sys,os
import neg
import argparse
import torch.utils.data as tdata
import utils
from tqdm import tqdm

def parse_args():
	'''
	Parses the heer arguments.
	'''
	parser = argparse.ArgumentParser(description="Run heer.")

	parser.add_argument('--more-param', nargs='?', default='None',
	                    help='customized parameter setting')

	parser.add_argument('--input', nargs='?', default='graph/karate.edgelist',
	                    help='Input graph path')

	parser.add_argument('--gpu', nargs='?', default='0',
	                    help='Embeddings path')

	parser.add_argument('--dimensions', type=int, default=128,
	                    help='Number of dimensions. Default is 128.')
	
	parser.add_argument('--batch-size', type=int, default=50,
	                    help='Batch size. Default is 50.')

	parser.add_argument('--window-size', type=int, default=1,
                    	help='Context size for optimization. Default is 10.')

	parser.add_argument('--pre-train-path', type=str, default='',
                    	help='embedding initialization')

	parser.add_argument('--build-graph', type=bool, default=False,
                    	help='heterogeneous information network construction')

	parser.add_argument('--graph-name', type=str, default='',
                    	help='prefix of dumped data')
	parser.add_argument('--data-dir', type=str, default='',
                    	help='data directory')
	parser.add_argument('--model-dir', type=str, default='',
                    	help='model directory')
	parser.add_argument('--test-dir', type=str, default='',
                    	help='test directory')

	parser.add_argument('--iter', default=500, type=int,
                      help='Number of epochs in SGD')
	parser.add_argument('--op', default=0, type=int)
	parser.add_argument('--map_func', default=0, type=int)
	parser.add_argument('--fast', default=1, type=int)
	parser.add_argument('--dump-timer', default=5, type=int)

	parser.add_argument('--weighted', dest='weighted', action='store_true',
	                    help='Boolean specifying (un)weighted. Default is unweighted.')
	parser.add_argument('--unweighted', dest='unweighted', action='store_false')
	parser.set_defaults(weighted=False)

	parser.add_argument('--directed', dest='directed', action='store_true',
	                    help='Graph is (un)directed. Default is undirected.')
	parser.add_argument('--undirected', dest='undirected', action='store_false')
	parser.set_defaults(directed=False)

	return parser.parse_args()

if __name__ == '__main__':
	args = parse_args()
	arg = {}
	_data = ''
	config_name = os.path.join(os.path.dirname(args.data_dir).replace('intermediate', 'input'), args.graph_name.split('_ko_')[0] + '.config')
	config = utils.read_config(config_name)
	#config['nodes'] = ['PR', 'AD', 'WO', 'AS', 'GE', 'PE', 'EV', 'PO']
	#config['edges'] = [(5, 2), (5, 5), (5, 2), (5, 2), (6, 1), (5, 5), (5, 3), (5, 1), (5, 3), (5, 7), (5, 2), (5, 4), (5, 1), (3, 1), (5, 3), (5, 1), (1, 1), (5, 0), (1, 1), (5, 1), (5, 1), (5, 5), (5, 5), (5, 2), (5, 5)]

	# baseline score
	if args.op == -1:
		_data = utils.load_emb(args.data_dir, args.pre_train_path, args.dimensions, args.graph_name, config['nodes'])
		#args.op = 1
	#print(_data)
	t.cuda.set_device(int(args.gpu))
	

	type_offset = cPickle.load(open(args.data_dir + args.graph_name + '_offset.p'))
	model = neg.NEG_loss(type_offset=type_offset, node_types=config['nodes'], edge_types=config['edges'], 
		embed_size=args.dimensions, pre_train_path=_data, graph_name=args.graph_name, 
		mode=args.op, map_mode=args.map_func)
	

	
	#print(model.in_embed.weight.sum())
	if args.op != -1:
		if args.more_param != 'None':
			model_path = args.model_dir + 'heer_' + args.graph_name + '_' + str(args.iter) + '_op_' + str(args.op) + \
				'_mode_' + str(args.map_func)+ '_' + args.more_param + '.pt'
		else:
			model_path = args.model_dir + 'heer_' + args.graph_name + '_' + str(args.iter) + '_op_' + str(args.op) + \
				'_mode_' + str(args.map_func)+ '.pt'
		print('model path:',model_path)
		xxx = t.load(model_path)
		#print('after')
		model.load_state_dict(xxx, False )
	model.eval()
	#if args.map_func == 1:
	#	model.map_mode = 0
		#print(model.parameters())

	#model.load_state_dict(t.load('/shared/data/qiz3/data/model/' +  args.model_name +'.pt'))
	#print(model.in_embed.weight.sum())
	#for el in model.edge_mapping:
	#	print(el, el.weight.data.cpu().numpy().tolist())
	#sys.exit(-1)
	
	print("Model Mode:", args.op)
	#pred_types = [0, 1, 2, 3, 4]
	suffix = '_' + args.graph_name + ('_eval_fast.txt' if args.fast == 1 else '_eval.txt')

	in_mapping = cPickle.load(open(args.data_dir + args.graph_name +'_in_mapping.p'))
	for idx, i in enumerate(config['types']):
		edge_prefix = []
		edge_prefix += (i, i+'-1')
		#print("Edge Type:", idx)
		#print(edge_prefix)
	
	#for el in model.edge_mapping:
	#	print(el, el.weight.data.cpu().numpy().tolist())
	#sys.exit(-1)

		tp = idx
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
						#print(line)
					#	continue

			if len(_input) == 0:
				print("no this type! in test")
				continue
			input_data = tdata.TensorDataset(t.LongTensor(_input), t.LongTensor(_output))
			#print(len(input_data))
			
			data_reader = tdata.DataLoader(input_data, args.batch_size, shuffle=False)
			score = []
			#model = neg.NEG_loss(type_offset=type_offset, node_types=args.node_types, edge_types=args.edge_types, embed_size=arg['emb_size'], pre_train_path=arg['pre_train'], graph_name=arg['graph_name'])
			#pbar = tqdm(total=len(data_reader) / args.batch_size)
			for i, data in enumerate(data_reader, 0):
				inputs, labels = data
				loss = model.predict(inputs, labels, tp, config['edges'][idx][0] == config['edges'][idx][1])
				score += loss
				#pbar.update(1)
			#pbar.close()

			with open(args.test_dir + prefix + suffix, 'r') as INPUT, open(args.test_dir + prefix + suffix.replace('eval', 'pred'), 'w') as OUTPUT:
				for i, line in enumerate(INPUT):
					node = line.strip().split(' ')
					_type_a, _id_a = node[0].split(':')
					_type_b, _id_b = node[1].split(':')
					assert _id_a in in_mapping[_type_a] and _id_b in in_mapping[_type_b]
					node[2] = str(score[i])
					OUTPUT.write(' '.join(node) + '\n')
				#assert cnt == len(score)
			

