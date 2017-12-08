import neg
import torch.optim as optim
import torch as t
import numpy as np
import torch.utils.data as tdata
import cPickle

#dict(, nn.Embedding)

# support heterogenous node type
# first consider about first order proximity
# different node type and edge type mapping function

class SkipGram(object):
	"""pytorch implementation for SkipGram"""
	def __init__(self, arg):
		super(SkipGram, self).__init__()
		type_offset = cPickle.load(open('/shared/data/qiz3/data/sample_offset.p'))
		self.neg_loss = neg.NEG_loss(type_offset=type_offset, types=['a', 'p', 'w', 'v', 'y', 'cp'],embed_size=arg['emb_size'])
		self.SGD = optim.SGD(self.neg_loss.parameters(), lr = 0.025)
		#self.walks = arg['walks']
		#self.input = cPickle.load(open('/shared/data/qiz3/data/input.p'))
		#self.output = cPickle.load(open('/shared/data/qiz3/data/output.p'))
		self.input = tdata.TensorDataset(t.LongTensor(cPickle.load(open('/shared/data/qiz3/data/sample_input.p'))), 
			t.LongTensor(cPickle.load(open('/shared/data/qiz3/data/sample_output.p'))))
		#self.output = utils.data.TensorDataset(cPickle.load(open('/shared/data/qiz3/data/output.p')))
		self.window_size = arg['window_size']
		self.data = tdata.DataLoader(self.input, 50)
		#self.walk_length = len(self.walks[0])
		self.iter = arg['iter']
		self.neg_ratio = arg['neg_ratio']
		
		
	def train(self):
		#return
		for epoch in xrange(self.iter):
			loss_sum = 0
			for i, data in enumerate(self.data, 0):
				inputs, labels = data
				loss = self.neg_loss(inputs, labels, self.neg_ratio)
				loss_sum += loss
				#print(loss)
				self.SGD.zero_grad()
				loss.backward()
				self.SGD.step()
			print(epoch, loss_sum)

	def output(self):
		word_embeddings = self.neg_loss.input_embeddings()