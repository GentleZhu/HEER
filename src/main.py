import argparse
import numpy as np
from emb_lib import SkipGram
import yago_network as nx
import torch as t
import cPickle
import utils
import torch.utils.data as tdata

YaGo_types = [(5, 2), (5, 5), (5, 2), (5, 2), (6, 1), (5, 5), (5, 3), (5, 1), (5, 3), (5, 7), (5, 2), (5, 4), (5, 1), (3, 1), (5, 3), 
		(5, 1), (1, 1), (5, 0), (1, 1), (5, 1), (5, 1), (5, 5), (5, 5), (5, 2), (5, 5)]
YaGo_nodes = ['PR', 'AD', 'WO', 'AS', 'GE', 'PE', 'EV', 'PO']
def parse_args():
	'''
	Parses the node2vec arguments.
	'''
	parser = argparse.ArgumentParser(description="Run node2vec.")

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

	parser.add_argument('--node-types', type=list, default=['PR', 'AD', 'WO', 'AS', 'GE', 'PE', 'EV', 'PO'])

	parser.add_argument('--edge-types', type=list, default=[(1,0),(1,1),(1,2), (1,3),(1,4)])
	#parser.add_argument('--edge-types', type=list, default=[(0,5),(1,5),(2,5),(3,5),(4,5)])

	parser.add_argument('--iter', default=500, type=int,
                      help='Number of epochs in SGD')
	parser.add_argument('--op', default=0, type=int)
	parser.add_argument('--map_func', default=0, type=int)
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


def learn_embeddings():
	'''
	Learn embeddings by optimizing the Skipgram objective using SGD.
	'''

	_data = utils.load_emb(args.pre_train_path, args.dimensions, args.graph_name, YaGo_nodes)
	_network = tdata.TensorDataset(t.LongTensor(cPickle.load(open(args.data_dir + args.graph_name + 'input.p'))), 
                               t.LongTensor(cPickle.load(open(args.data_dir + args.graph_name + 'output.p'))))
	model = SkipGram({'emb_size':args.dimensions,
		'window_size':1, 'batch_size':args.batch_size, 'iter':args.iter, 'neg_ratio':5,
		'graph_name':args.graph_name, 'dump_timer':args.dump_timer, 'model_dir':args.model_dir,
		'data_dir':args.data_dir, 'mode':args.op, 'map_mode':args.map_func,
		'lr_ratio':16, 'lr': 2.5, 'network':_network,
		'pre_train':_data, 'node_types':YaGo_nodes, 'edge_types':YaGo_types})
	

	model.train()
	
	return

def main(args):
	'''
	Pipeline for representational learning for all nodes in a graph.
	'''
	if args.build_graph:
		#print(args.node_types)
		tmp = nx.HinLoader({'graph': args.input, 'types':YaGo_nodes, 'edge_types':YaGo_types})
		tmp.readHin()
		tmp.encode()
		tmp.dump(args.data_dir + args.graph_name)
		#print(args.edge_types)
	else:
		learn_embeddings()

#for YaGo
def load_aspect(args):
	total_types = [(5, 2), (5, 5), (5, 2), (5, 2), (6, 1), (5, 5), (5, 3), (5, 1), (5, 3), 
	(5, 7), (5, 2), (5, 4), (5, 1), (3, 1), (5, 3), (5, 1), (1, 1), (5, 0), (1, 1), (5, 1), 
	(5, 1), (5, 5), (5, 5), (5, 2), (5, 5)]
	#edge_type_id = ['3' , '13', '17', '10', '33', '1' , '11', '2' , '26', '31', '29', '30', '35', '9' , '27', '25', '20', '36', '12', '6' , '39', '15', '38', '21']
	edge_type_id = ['25', '26', '27', '20', '21', '29', '1', '3', '2', '6', '9', '8', '13', '38', '11', '10', '39', '12', '15', '17', '33', '31', '30', '36', '35']
	aspects = {
		'PE-LOC':['26', '29', '15', '39', '13', '10'],
		'PE-WO':['20', '25', '27', '9', '36'],
		'complex':['15', '39', '38', '1', '33', '13', '10', '6']
	}
	for aspect in aspects:
		tmp = nx.HinLoader({'graph': args.input, 'types':args.node_types, 'edge_types':total_types, 'edge_ids':aspects[aspect]})
		tmp.readHin()
		tmp.encode()
		tmp.dump('/shared/data/qiz3/data/' + args.graph_name+aspect+'_')

if __name__ == "__main__":
	args = parse_args()
	#read_hin(args.input)
	t.cuda.set_device(int(args.gpu))
	main(args)
	#load_aspect(args)
