import cPickle

class HinLoader(object):
	"""docstring for HinLoader"""
	def __init__(self, arg):
		self.in_mapping = dict()
		self.out_mapping = dict()
		self.input = list()
		self.output = list()
		self.arg = arg
		self.edge_stat = [0] * len(self.arg['edge_types'])
		#print(arg['types'])
		for k in arg['types']:
			self.in_mapping[k] = dict()
			self.out_mapping[k] = dict()
		#print(self.in_mapping.keys())
		#print(self.out_mapping.keys())

	def inNodeMapping(self, key, type):
		if key not in self.in_mapping[type]:
			self.out_mapping[type][len(self.in_mapping[type])] = key
			self.in_mapping[type][key] = len(self.in_mapping[type])

		return self.in_mapping[type][key]

	def readHin(self):
		#num_nodes = defaultdict(int)
		_edge_types = ['25', '26', '27', '20', '21', '29', '1', '3', '2', '6', '9', '8', '13', '38', '11', '10', '39', '12', '15', '17', '33', '31', '30', '36', '35']
		assert len(_edge_types) == len(self.arg['edge_types'])
		with open(self.arg['graph']) as INPUT:
			for line in INPUT:
				edge = line.strip().split(' ')
				if edge[-1] not in _edge_types:
					continue
				node_a = edge[0].split(':')
				node_b = edge[1].split(':')
				node_a_type = self.arg['types'].index(node_a[0])
				node_b_type = self.arg['types'].index(node_b[0])
				edge_type = _edge_types.index(edge[-1])
				assert edge_type != 11
				self.edge_stat[edge_type] += 1
				assert (node_a_type, node_b_type) == self.arg['edge_types'][edge_type]
				self.input.append([edge_type, self.inNodeMapping(node_a[1], node_a[0])])
				self.output.append([self.arg['types'].index(node_b[0]), self.inNodeMapping(node_b[1], node_b[0])])
	
	def encode(self):
		self.encoder = dict()
		offset = 0
		for k in self.arg['types']:
			#print(k)
			self.encoder[k] = offset
			offset += len(self.in_mapping[k])
		self.encoder['sum'] = offset
		print(self.encoder)
		for i,ie in enumerate(self.input):
			self.input[i][1] += self.encoder[self.arg['types'][self.arg['edge_types'][ie[0]][0]]]
		for i,ie in enumerate(self.output):
			self.output[i][1] += self.encoder[self.arg['types'][ie[0]]]
			

	def dump(self, dump_path):
		print(self.edge_stat)
		cPickle.dump(self.encoder, open(dump_path + 'offset.p', 'wb'))
		cPickle.dump(self.input, open(dump_path + 'input.p', 'wb'))
		cPickle.dump(self.output, open(dump_path + 'output.p', 'wb'))
		cPickle.dump(self.in_mapping, open(dump_path + 'in_mapping.p', 'wb'))
		cPickle.dump(self.out_mapping, open(dump_path + 'out_mapping.p', 'wb'))
		cPickle.dump(self.edge_stat, open(dump_path + 'edge_stat.p', 'wb'))