import neg
import torch.optim as optim
import torch as t
import numpy as np
import torch.utils.data as tdata
import utils
import math
import cPickle
from tqdm import tqdm

# support heterogenous node type
# first consider about first order proximity
# different node type and edge type mapping function

class SkipGram(object):
	"""pytorch implementation for SkipGram"""
	def __init__(self, arg):
		super(SkipGram, self).__init__()
		type_offset = cPickle.load(open('/shared/data/qiz3/data/' + arg['graph_name'] + 'offset.p'))
		self.neg_loss = neg.NEG_loss(type_offset=type_offset, node_types=arg['node_types'], edge_types=arg['edge_types'], embed_size=arg['emb_size'], pre_train_path=arg['pre_train'], graph_name=arg['graph_name'], mode=arg['mode'])
		self.input = arg['network']
		#print('edge layer learning rate is:', arg['lr'] * (float(len(arg['edge_types'])) / type_offset['sum']))
		edge_stats = cPickle.load(open('/shared/data/qiz3/data/' + arg['graph_name'] + 'edge_stat.p'))
		#print(edge_stats)
		_params = [{'params': self.neg_loss.in_embed.parameters()}, 
			{'params': self.neg_loss.out_embed.parameters()}]
		#for param in self.neg_loss.in_embed.parameters():
		#	param.requires_grad = False
		#for param in self.neg_loss.out_embed.parameters():
		#	param.requires_grad = False
		#_params = []
		for i in xrange(len(self.neg_loss.edge_mapping)):
			_params.append({'params': self.neg_loss.edge_mapping[i].parameters(), 
				'lr': arg['lr'] * arg['lr_ratio'] * (float(len(self.input))) / (type_offset['sum'] * edge_stats[i])})
		self.SGD = optim.SGD(_params, lr = arg['lr'])
		#self.SGD = optim.SGD(self.neg_loss.edge_mapping.parameters(), lr = 0.25)
		#self.SGD = optim.SGD(self.neg_loss.parameters(), lr = arg['lr'])
		#print(self.neg_loss.edge_mapping)
		
		#self.input = tdata.TensorDataset(t.LongTensor(cPickle.load(open('/shared/data/qiz3/data/' + arg['graph_name'] + 'input.p'))), 
		#	t.LongTensor(cPickle.load(open('/shared/data/qiz3/data/' + arg['graph_name'] + 'output.p'))))

		self.window_size = arg['window_size']
		self.data = tdata.DataLoader(self.input, arg['batch_size'], shuffle=True)
		self.batch_size = arg['batch_size']
		self.iter = arg['iter']
		self.neg_ratio = arg['neg_ratio']
	
	def get_params(self):		
		for param in self.neg_loss.in_emb.parameters():
			yield param

	def train(self):
		#return
		#clip_params = self.get_params()
		#print(self.neg_loss.in_emb.parameters())

		for epoch in xrange(self.iter):
			loss_sum = 0
			#pbar = tqdm(total=len(self.input) / self.batch_size)
			
			#i_sum = []
			#o_sum = []
			#e_sum = []
			for i, data in tqdm(enumerate(self.data, 0), total = len(self.input) / self.batch_size):
				inputs, labels = data
				loss, pure_loss = self.neg_loss(inputs, labels, self.neg_ratio)
				
				if np.isnan(loss.data.cpu().numpy()):
					return -1
				loss_sum += pure_loss * self.batch_size
				self.SGD.zero_grad()
				
				loss.backward()
				
				utils.clip_sparse_grad_norm(self.neg_loss.in_embed.parameters(), 0.1)
				utils.clip_sparse_grad_norm(self.neg_loss.out_embed.parameters(), 0.1)
				
				for i in xrange(len(self.neg_loss.edge_mapping)):
					utils.clip_grad_norm(self.neg_loss.edge_mapping[i].parameters(), 0.1)

				self.SGD.step()
				

			if epoch % 5 == 0:
				t.save(self.neg_loss.state_dict(), '/shared/data/qiz3/data/model/dblp_0.1_' + str(epoch) + '_heer.pt')
			#if epoch % 20 == 0:
			#print(num_batches)
			print(epoch, loss_sum)
			#return i_sum, o_sum, e_sum
			#pbar.close()
				#print(self.neg_loss.input_embeddings()[0,:])
			#print(epoch, loss_sum)

	def output(self):
		word_embeddings = self.neg_loss.input_embeddings()