import cPickle

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