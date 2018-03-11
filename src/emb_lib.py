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
		type_offset = cPickle.load(open(arg['data_dir'] + arg['graph_name'] + '_offset.p'))
		self.neg_loss = neg.NEG_loss(type_offset=type_offset, node_types=arg['node_types'], edge_types=arg['edge_types'], 
			embed_size=arg['emb_size'], pre_train_path=arg['pre_train'], 
			graph_name=arg['graph_name'], mode=arg['mode'], map_mode=arg['map_mode'])
		self.input = arg['network']
		#print('edge layer learning rate is:', arg['lr'] * (float(len(arg['edge_types'])) / type_offset['sum']))
		edge_stats = cPickle.load(open(arg['data_dir'] + arg['graph_name'] + '_edge_stat.p'))
		#print(edge_stats)
		self.mode = arg['mode']
		self.map_mode = arg['map_mode']
		self.dump_timer = arg['dump_timer']
		self.model_dir = arg['model_dir']
		#enable batch normalization
		if self.map_mode == 0:
			_params = [{'params': self.neg_loss.in_embed.parameters()}, 
				{'params': self.neg_loss.out_embed.parameters()}]
			for i in xrange(len(self.neg_loss.edge_mapping)):
				_params.append({'params': self.neg_loss.edge_mapping[i].parameters(),
					#'lr': arg['lr']})
					'lr': arg['lr'] * arg['lr_ratio'] * (float(len(self.input))) / (type_offset['sum'] * edge_stats[i] + 1e-6)})
			self.SGD = optim.SGD(_params, lr = arg['lr'])
			#self.edge_lr_ratio = arg['lr_ratio']
		else:
			# mode <=0, with 
			self.SGD = optim.SGD(self.neg_loss.parameters(), lr = arg['lr'])

		self.window_size = arg['window_size']
		self.graph_name = arg['graph_name']
		
		self.data = tdata.DataLoader(self.input, arg['batch_size'], shuffle=True)
		self.batch_size = arg['batch_size']
		self.iter = arg['iter']
		self.neg_ratio = arg['neg_ratio']
	
	def get_params(self):		
		for param in self.neg_loss.in_emb.parameters():
			yield param

	def train(self):
		with open(self.model_dir + 'heer_' + self.graph_name + '_op_' + str(self.mode) + 
						'_mode_' + str(self.map_mode)+ '.log', 'w') as LOG:
			for epoch in xrange(self.iter):
				loss_sum = 0

				for i, data in enumerate(self.data, 0):
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
					

				if epoch % self.dump_timer == 0:
					t.save(self.neg_loss.state_dict(), self.model_dir + 'heer_' + self.graph_name + '_' + str(epoch) + '_op_' + str(self.mode) + 
						'_mode_' + str(self.map_mode)+ '.pt')

				LOG.write(str(epoch) + '\t' + str(np.asscalar(loss_sum.data.cpu().numpy())) + '\n')
				LOG.flush()
				
			#return i_sum, o_sum, e_sum
			#pbar.close()
				#print(self.neg_loss.input_embeddings()[0,:])
			#print(epoch, loss_sum)

	def output(self):
		word_embeddings = self.neg_loss.input_embeddings()
