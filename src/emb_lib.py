import neg
import torch.optim as optim
import torch as t
import numpy as np
import torch.utils.data as tdata
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
		self.neg_loss = neg.NEG_loss(type_offset=type_offset, node_types=arg['node_types'], edge_types=arg['edge_types'], embed_size=arg['emb_size'], pre_train_path=arg['pre_train'], graph_name=arg['graph_name'])
		
		self.SGD = optim.SGD(self.neg_loss.parameters(), lr = 0.1)
		self.input = tdata.TensorDataset(t.LongTensor(cPickle.load(open('/shared/data/qiz3/data/' + arg['graph_name'] + 'input.p'))), 
			t.LongTensor(cPickle.load(open('/shared/data/qiz3/data/' + arg['graph_name'] + 'output.p'))))

		self.window_size = arg['window_size']
		self.data = tdata.DataLoader(self.input, arg['batch_size'], shuffle=True)
		self.batch_size = arg['batch_size']
		self.iter = arg['iter']
		self.neg_ratio = arg['neg_ratio']
	
	def train(self):
		#return
		clip_params = self.get_params()
		for epoch in xrange(self.iter):
			loss_sum = 0
			pbar = tqdm(total=len(self.input) / self.batch_size)
			for i, data in enumerate(self.data, 0):
				inputs, labels = data
				pbar.update(1)
				#print(inputs[:,1])
				#print(labels[:,1:].contiguous().view(-1))
				loss = self.neg_loss(inputs, labels, self.neg_ratio)
				loss_sum += self.batch_size * loss
				self.SGD.zero_grad()
				loss.backward()
				self.SGD.step()
				#t.nn.utils.clip_grad_norm(self.get_params(), 0.25)

			if epoch % 1 == 0:
				t.save(self.neg_loss, '/shared/data/qiz3/data/model/diag_'+str(epoch)+'.pt')
			#if epoch % 20 == 0:
			#print(num_batches)
			print(epoch, loss_sum)
			pbar.close()
				#print(self.neg_loss.input_embeddings()[0,:])
			#print(epoch, loss_sum)

	def output(self):
		word_embeddings = self.neg_loss.input_embeddings()