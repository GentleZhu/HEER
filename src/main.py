import argparse
import numpy as np
from emb_lib import SkipGram
from collections import defaultdict
import network as nx
import torch
import cPickle

def parse_args():
	'''
	Parses the node2vec arguments.
	'''
	parser = argparse.ArgumentParser(description="Run node2vec.")

	parser.add_argument('--input', nargs='?', default='graph/karate.edgelist',
	                    help='Input graph path')

	parser.add_argument('--gpu', nargs='?', default='0',
	                    help='Embeddings path')

	parser.add_argument('--output', nargs='?', default='emb/karate.emb',
	                    help='Embeddings path')

	parser.add_argument('--dimensions', type=int, default=128,
	                    help='Number of dimensions. Default is 128.')
	
	parser.add_argument('--batch-size', type=int, default=50,
	                    help='Batch size. Default is 50.')

	parser.add_argument('--window-size', type=int, default=10,
                    	help='Context size for optimization. Default is 10.')

	parser.add_argument('--initialization', type=str, default='',
                    	help='embedding initialization')

	parser.add_argument('--iter', default=500, type=int,
                      help='Number of epochs in SGD')

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
	#walks = [map(lambda x: x-1, walk) for walk in walks]
	#model = Word2Vec(walks, size=args.dimensions, window=args.window_size, min_count=0, sg=1, workers=args.workers, iter=args.iter)
	#print model
	model = SkipGram({'emb_size':args.dimensions, \
		'window_size':args.window_size, 'batch_size':args.batch_size, 'iter':args.iter, 'neg_ratio':5, 
		'pre_train':'/shared/data/qiz3/data/dim_100_attr_nodes_apvwy.emb'})
	model.train()
	#model.save_word2vec_format(args.output)
	
	return

def main(args):
	'''
	Pipeline for representational learning for all nodes in a graph.
	'''
	if False:
		tmp = nx.HinLoader({'graph': args.input, 'types':['a', 'p', 'w', 'v', 'y', 'cp']})
		tmp.readHin()
		tmp.encode()
		tmp.dump('/shared/data/qiz3/data/')
	
	learn_embeddings()

if __name__ == "__main__":
	args = parse_args()
	#read_hin(args.input)
	torch.cuda.set_device(int(args.gpu))
	main(args)
