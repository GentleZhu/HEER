import neg
#import neg_naive as neg
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
		type_offset = cPickle.load(open('/shared/data/qiz3/data/offset.p'))
		self.neg_loss = neg.NEG_loss(type_offset=type_offset, node_types=['a', 'p', 'w', 'v', 'y', 'cp'],edge_types=[(0,5), (1,5), (2,5), (3,5), (4,5)], embed_size=arg['emb_size'], pre_train_path=arg['pre_train'])
		#self.neg_loss = neg.NEG_loss(num_classes=type_offset['sum'],embed_size=arg['emb_size'])
		
		self.SGD = optim.SGD(self.neg_loss.parameters(), lr = 0.25)
		#self.walks = arg['walks']
		#self.input = cPickle.load(open('/shared/data/qiz3/data/input.p'))
		#self.output = cPickle.load(open('/shared/data/qiz3/data/output.p'))
		self.input = tdata.TensorDataset(t.LongTensor(cPickle.load(open('/shared/data/qiz3/data/input.p'))), 
			t.LongTensor(cPickle.load(open('/shared/data/qiz3/data/output.p'))))
		#self.output = utils.data.TensorDataset(cPickle.load(open('/shared/data/qiz3/data/output.p')))
		self.window_size = arg['window_size']
		self.data = tdata.DataLoader(self.input, arg['batch_size'])
		self.batch_size = arg['batch_size']
		self.iter = arg['iter']
		self.neg_ratio = arg['neg_ratio']
		#if len(arg['pre_train']) > 0:
		#	in_mapping = cPickle.load(open('/shared/data/qiz3/data/in_mapping.p'))	
	
	def train(self):
		#return
		for epoch in xrange(self.iter):
			loss_sum = 0
			for i, data in enumerate(self.data, 0):
				inputs, labels = data
				#print(inputs[:,1])
				#print(labels[:,1:].contiguous().view(-1))
				loss = self.neg_loss(inputs, labels, self.neg_ratio)
				loss_sum += self.batch_size * loss
				#print(loss)
				self.SGD.zero_grad()
				loss.backward()
				self.SGD.step()
				for layer_i in len(self.neg_loss.edge_mapping):
					print(self.neg_loss.edge_mapping[layer_i].weight.data)
				#if i % 10000 == 9999:
				#	print(epoch,i,loss_sum / i)
					#break
			if epoch % 10 == 0:
				t.save(self.neg_loss, '/shared/data/qiz3/data/model/diag_'+str(epoch)+'.pt')
			#if epoch % 20 == 0:
			#print(num_batches)
			print(epoch, loss_sum)
				#print(self.neg_loss.input_embeddings()[0,:])
			#print(epoch, loss_sum)

	def output(self):
		word_embeddings = self.neg_loss.input_embeddings()