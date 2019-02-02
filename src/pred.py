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

def load_mapping(input_file):
	id2name = dict()
	with open(input_file) as IN:
		for line in IN:
			tmp = line.strip().split('\t')
			id2name[int(tmp[1])] = tmp[0]
	return id2name

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
	in_mapping = cPickle.load(open(args.data_dir + args.graph_name + '_in_mapping.p'))
	out_mapping = cPickle.load(open(args.data_dir + args.graph_name + '_out_mapping.p'))
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
		xxx = t.load(model_path, map_location=lambda storage, loc: storage)
		model.load_state_dict(xxx, False )
		out_emb = model.output_embeddings()
		
		offset,prev_offset = 0,0
		print(type_offset)
		with open(args.data_dir + 'heer_' + args.graph_name + '_' + str(args.iter) + '_op_' + str(args.op) + \
				'_mode_' + str(args.map_func)+ '_' + args.more_param + '.emb', 'w') as OUT:
			num_nodes, num_dim = out_emb.shape
			OUT.write(str(num_nodes)+' '+str(num_dim)+'\n')
			config['nodes'].append('sum')
			for idx,t in enumerate(config['nodes']):
				if t == 'sum':
					break
				tp = config['nodes'][idx+1]
				while offset < type_offset[tp]:
					OUT.write("{}:{} {}\n".format(t, out_mapping[t][offset-prev_offset], ' '.join(map(str,out_emb[offset].tolist())) ))
					offset += 1
				prev_offset = type_offset[tp]
				#	out_mapping[]
            #type_offset[tp]



		#print(type_offset['D'])
		#print("{} {}".format(len(in_mapping['D'])+len(in_mapping['P']), 100))
		#id2name = load_mapping('/shared/data/qiz3/text_summ/intermediate_data/nyt13_10k_9_25_kb.node')
		#for i in range(type_offset['D'], type_offset['D'] + len(in_mapping['D'])):
		#	print("{} {}".format(id2name[int(out_mapping['D'][i - type_offset['D']])], ' '.join(map(str,out_emb[i].tolist())) ))
			#break
		#for i in range(type_offset['P'], type_offset['P'] + len(in_mapping['P'])):
		#	print("{} {}".format(id2name[int(out_mapping['P'][i - type_offset['P']])], ' '.join(map(str,out_emb[i].tolist())) ))
