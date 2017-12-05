import neg
import torch.optim as optim
import torch as t
import numpy as np

# support heterogenous node type
# first consider about first order proximity
# different node type and edge type mapping function

class SkipGram(object):
	"""pytorch implementation for SkipGram"""
	def __init__(self, arg):
		super(SkipGram, self).__init__()
		self.neg_loss = neg.NEG_loss(num_classes=arg['num_nodes'], embed_size=arg['emb_size'])
		self.SGD = optim.SGD(self.neg_loss.parameters(), lr = 0.025)
		self.walks = arg['walks']
		self.window_size = arg['window_size']
		self.walk_length = len(self.walks[0])
		self.iter = arg['iter']
		self.neg_ratio = arg['neg_ratio']
		print self.walk_length
		
	def train(self):
		for iter in xrange(self.iter):
			np.random.shuffle(self.walks)
			for i,walk in enumerate(self.walks):
				train_input_batch = np.array([walk[j] for j in xrange(self.walk_length - self.window_size)])
				train_ctx_batch = np.array([walk[j+1:j+1+self.window_size] for j in xrange(self.walk_length-self.window_size)])
				loss = self.neg_loss(t.from_numpy(train_input_batch),\
					t.from_numpy(train_ctx_batch), self.neg_ratio)
				batches = iter*len(self.walks)+i
				if batches % 100 == 0:
					print "iter:",iter," loss:",loss," batches:",batches
				self.SGD.zero_grad()
				loss.backward()
				self.SGD.step()

	def output(self):
		word_embeddings = self.neg_loss.input_embeddings() 
