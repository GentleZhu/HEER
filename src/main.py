import argparse
import numpy as np
from emb_lib import SkipGram
from collections import defaultdict
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

	parser.add_argument('--walk-length', type=int, default=80,
	                    help='Length of walk per source. Default is 80.')

	parser.add_argument('--num-walks', type=int, default=10,
	                    help='Number of walks per source. Default is 10.')

	parser.add_argument('--window-size', type=int, default=10,
                    	help='Context size for optimization. Default is 10.')

	parser.add_argument('--iter', default=10, type=int,
                      help='Number of epochs in SGD')

	parser.add_argument('--workers', type=int, default=8,
	                    help='Number of parallel workers. Default is 8.')

	parser.add_argument('--p', type=float, default=1,
	                    help='Return hyperparameter. Default is 1.')

	parser.add_argument('--q', type=float, default=1,
	                    help='Inout hyperparameter. Default is 1.')

	parser.add_argument('--weighted', dest='weighted', action='store_true',
	                    help='Boolean specifying (un)weighted. Default is unweighted.')
	parser.add_argument('--unweighted', dest='unweighted', action='store_false')
	parser.set_defaults(weighted=False)

	parser.add_argument('--directed', dest='directed', action='store_true',
	                    help='Graph is (un)directed. Default is undirected.')
	parser.add_argument('--undirected', dest='undirected', action='store_false')
	parser.set_defaults(directed=False)

	return parser.parse_args()

class HinLoader(object):
	"""docstring for HinLoader"""
	def __init__(self, arg):
		self.in_mapping = dict()
		self.out_mapping = dict()
		self.input = list()
		self.output = list()
		self.arg = arg
		for k in arg['types']:
			self.in_mapping[k] = dict()
			self.out_mapping[k] = dict()
		print(self.in_mapping.keys())
		print(self.out_mapping.keys())

	def inNodeMapping(self, key, type):
		if key not in self.in_mapping[type]:
			self.out_mapping[type][len(self.in_mapping[type])] = key
			self.in_mapping[type][key] = len(self.in_mapping[type])

		return self.in_mapping[type][key]

	def readHin(self):
		#num_nodes = defaultdict(int)
		with open(self.arg['graph']) as INPUT:
			for line in INPUT:
				edge = line.strip().split(' ')
				node_a = edge[0].split(':')
				node_b = edge[1].split(':')
				self.input.append([self.arg['types'].index(node_a[0]), self.inNodeMapping(node_a[1], node_a[0])])
				self.output.append([self.arg['types'].index(node_b[0]), self.inNodeMapping(node_b[1], node_b[0])])
				#self.input.append([self.arg['types'].index(node_a[0]), self.arg['types'].index(node_b[0]), self.inNodeMapping(node_a[1], node_a[0]), self.inNodeMapping(node_b[1], node_b[0])])
				#self.graph[(node_a[0], node_b[0])].append((self.inNodeMapping(node_a[1], node_a[0]), self.inNodeMapping(node_b[1], node_b[0])))
		#print(map(lambda x:len(x), self.in_mapping))
	
	def encode(self):
		self.encoder = dict()
		offset = 0
		for k in self.in_mapping:
			self.encoder[k] = offset
			offset += len(self.in_mapping[k])
		self.encoder['sum'] = offset
		print(self.encoder)
		for i,ie in enumerate(self.input):
			self.input[i][1] += self.encoder[self.arg['types'][ie[0]]]
		for i,ie in enumerate(self.output):
			self.output[i][1] += self.encoder[self.arg['types'][ie[0]]]
			

	def dump(self, dump_path):
		cPickle.dump(self.encoder, open(dump_path + 'offset.p', 'wb'))
		cPickle.dump(self.input, open(dump_path + 'input.p', 'wb'))
		cPickle.dump(self.output, open(dump_path + 'output.p', 'wb'))
		cPickle.dump(self.in_mapping, open(dump_path + 'in_mapping.p', 'wb'))
		cPickle.dump(self.out_mapping, open(dump_path + 'out_mapping.p', 'wb'))

		

def read_hin(graph_name):
	graph = defaultdict(list)
	num_nodes = defaultdict(int)
	with open(graph_name) as INPUT:
		for line in INPUT:
			edge = line.strip().split(' ')
			node_a = edge[0].split(':')
			node_b = edge[1].split(':')
			graph[(node_a[0], node_b[0])].append((int(node_a[1]), int(node_b[1])))
			num_nodes[node_a[0]] = max(num_nodes[node_a[0]], int(node_a[1]))
			num_nodes[node_b[0]] = max(num_nodes[node_b[0]], int(node_b[1]))
	print(num_nodes)
	return graph,num_nodes



def read_graph():
	'''
	Reads the input network in networkx.
	'''
	if args.weighted:
		G = nx.read_edgelist(args.input, nodetype=int, data=(('weight',float),), create_using=nx.DiGraph())
	else:
		G = nx.read_edgelist(args.input, nodetype=int, create_using=nx.DiGraph())
		for edge in G.edges():
			G[edge[0]][edge[1]]['weight'] = 1

	if not args.directed:
		G = G.to_undirected()

	return G

def learn_embeddings():
	'''
	Learn embeddings by optimizing the Skipgram objective using SGD.
	'''
	#walks = [map(lambda x: x-1, walk) for walk in walks]
	#model = Word2Vec(walks, size=args.dimensions, window=args.window_size, min_count=0, sg=1, workers=args.workers, iter=args.iter)
	#print model
	model = SkipGram({'emb_size':args.dimensions, \
		'window_size':args.window_size, 'iter':args.iter, 'neg_ratio':5})
	model.train()
	#model.save_word2vec_format(args.output)
	
	return

def main(args):
	'''
	Pipeline for representational learning for all nodes in a graph.
	'''
	#tmp = HinLoader({'graph': args.input, 'types':['a', 'p', 'w', 'v', 'y', 'cp']})
	#tmp.readHin()
	#tmp.encode()
	#tmp.dump('/shared/data/qiz3/data/')
	#G = node2vec.Graph(nx_G, args.directed, args.p, args.q)
	#G.preprocess_transition_probs()
	#walks = G.simulate_walks(args.num_walks, args.walk_length)
	learn_embeddings()

if __name__ == "__main__":
	args = parse_args()
	#read_hin(args.input)
	torch.cuda.set_device(int(args.gpu))
	main(args)
	#nx_G = read_graph()
