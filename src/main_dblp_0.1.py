import sys
import utils
from emb_lib import SkipGram
import torch as t
import torch.utils.data as tdata
import cPickle
args = {'emb_size':128, 'window_size':1, 'batch_size':128, 'iter':40, 'neg_ratio':5, 'graph_name':'dblp_0.1_',
       'pre_train_path':'/shared/data/yushi2/edge_rep_codes/intermediate_data/dblp_0.1_out_line_samples200000_dim128.emb',
       'node_types':['A','P','Y','W','V'], 'edge_types':[(1,0),(1,1),(1,2),(1,3),(1,4)], 'gpu':1, 'lr':2.5, 'mode': 1}

t.cuda.set_device(int(args['gpu']))
t.cuda.empty_cache()
_data = utils.load_emb(args['pre_train_path'], args['emb_size'], args['graph_name'], args['node_types'])
_network = tdata.TensorDataset(t.LongTensor(cPickle.load(open('/shared/data/qiz3/data/' + args['graph_name'] + 'input.p'))), 
                               t.LongTensor(cPickle.load(open('/shared/data/qiz3/data/' + args['graph_name'] + 'output.p'))))

model = SkipGram({'emb_size':args['emb_size'],
                  'window_size':1, 'batch_size':args['batch_size'], 'iter':args['iter'], 'neg_ratio':args['neg_ratio'],
                  'graph_name': args['graph_name'], 'mode': args['mode'],
                  'pre_train':_data, 'node_types':args['node_types'], 'lr_ratio':16,
                  'edge_types':args['edge_types'], 'lr':args['lr'], 'network':_network})
model.train()