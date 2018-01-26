import torch as t
import numpy as np
import cPickle
import sys
import neg

if __name__ == '__main__':
	model = t.load('/shared/data/qiz3/data/model/diag_' + sys.argv[1] +'.pt')
	edge_type = 
	in_mapping = cPickle.load(open('/shared/data/qiz3/data/' + prefix +'in_mapping.p'))
	with open(, 'r') as INPUT:
		_input = []
		_output = []
		for line in INPUT:
            node = line.strip().split(' ')
            _type_a, _id_a = node[0].split(':')
            _type_b, _id_b = node[1].split(':')

            _input.append(in_mapping[_type_a][_id_a] + self.type_offset[node_types.index(_type_a)])
            _output.append(in_mapping[_type_b][_id_b] + self.type_offset[node_types.index(_type_b)])

        input_data = tdata.TensorDataset(t.LongTensor(_input), t.LongTensor(_output))
        data = tdata.DataLoader(self.input, arg['batch_size'], shuffle=False)
        model = neg.NEG_loss(type_offset=type_offset, node_types=arg['node_types'], edge_types=arg['edge_types'], embed_size=arg['emb_size'], pre_train_path=arg['pre_train'], graph_name=arg['graph_name'])
        for i, data in enumerate(data, 0):
			inputs, labels = data
			loss = model.predict(inputs, labels)