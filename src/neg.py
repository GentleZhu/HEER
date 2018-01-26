import torch as t
import torch.nn as nn
from torch.autograd import Variable
from torch.nn import Parameter
import numpy as np
import cPickle
import utils


class NEG_loss(nn.Module):
    def __init__(self, type_offset, node_types, edge_types, embed_size, pre_train_path, graph_name = '', weights=None):
        """
        :param num_classes: An int. The number of possible classes.
        :param embed_size: An int. EmbeddingLockup size
        :param num_sampled: An int. The number of sampled from noise examples
        :param weights: A list of non negative floats. Class weights. None if
            using uniform sampling. The weights are calculated prior to
            estimation and can be of any form, e.g equation (5) in [1]
        """

        super(NEG_loss, self).__init__()

        self.num_classes = type_offset['sum']
        self.type_offset = []
        for tp in node_types:
            self.type_offset.append(type_offset[tp])

        self.edge_types = edge_types
        self.embed_size = embed_size
        self.in_embed = nn.Embedding(self.num_classes, self.embed_size, sparse=True)

        self.edge_mapping = nn.ModuleList()
        self.out_embed = nn.Embedding(self.num_classes, self.embed_size, sparse=True)

        self.out_embed.weight = Parameter(t.FloatTensor(self.num_classes, self.embed_size).uniform_(-1, 1).cuda())
        self.in_embed.weight = Parameter(t.FloatTensor(self.num_classes, self.embed_size).uniform_(-1, 1).cuda())
        #self.out_embed.weight = Parameter(t.FloatTensor(self.num_classes, self.embed_size).uniform_(-1, 1))
        #self.in_embed.weight = Parameter(t.FloatTensor(self.num_classes, self.embed_size).uniform_(-1, 1))
        #self.out_embed.weight.requires_grad = False
        #self.in_embed.weight.requires_grad = False

        if len(pre_train_path) > 0:
            #print(self.type_offset)
            in_mapping = cPickle.load(open('/shared/data/qiz3/data/' + graph_name +'in_mapping.p'))
            print(len(in_mapping))
            with open(pre_train_path, 'r') as INPUT:
                INPUT.readline()
                #pre_train_emb = np.random.rand(self.num_classes, self.embed_size)
                #pre_trained_list = set()
                for line in INPUT:
                    node = line.strip().split(' ')
                    _type, _id = node[0].split(':')
                    _index = in_mapping[_type][_id] + self.type_offset[node_types.index(_type)]
                    self.out_embed.weight.data[_index, :] = t.FloatTensor(map(lambda x:float(x), node[1:]))
                    self.in_embed.weight.data[_index, :] = t.FloatTensor(map(lambda x:float(x), node[1:]))
                #self.out_embed.weight.data.renorm_(2,0,1)
                #self.in_embed.weight.data.renorm_(2,0,1)
                    #pre_trained_list.add(_index)
                    #pre_train_emb[_index] = np.asarray(map(lambda x:float(x), node[1:]))
                #print(len(pre_trained_list))
            #self.out_embed.weight.data.copy_(t.from_numpy(pre_train_emb))
            #self.in_embed.weight.data.copy_(t.from_numpy(pre_train_emb))
            #self.edge_mapping.append(nn.Linear(self.embed_size, self.embed_size, bias=False).cuda())
        print(self.in_embed.weight.sum())
        if True:
            for tp in edge_types:
                self.edge_mapping.append(utils.DiagLinear(self.embed_size).cuda())
                #self.edge_mapping.append(utils.SymmLinear(self.embed_size).cuda())
                #self.edge_mapping[-1].weight = Parameter(t.FloatTensor(self.embed_size, self.embed_size).uniform_(-1, 1).cuda())
                self.edge_mapping[-1].weight = Parameter(t.FloatTensor(self.embed_size).uniform_(-1, 1).cuda())
        
        self.type_offset.append(type_offset['sum'])
        print(self.type_offset)
        print(self.num_classes)
        #print(self.type_offset)

        self.weights = weights
        if self.weights is not None:
            assert min(self.weights) >= 0, "Each weight should be >= 0"

            self.weights = Variable(t.from_numpy(weights)).float()

    def sample(self, num_sample):
        """
        draws a sample from classes based on weights
        """
        return t.multinomial(self.weights, num_sample, True)

    def forward(self, input_labels, out_labels, num_sampled):
        """
        :param input_labels: Tensor with shape of [batch_size] of Long type
        :param out_labels: Tensor with shape of [batch_size, window_size] of Long type
        :param num_sampled: An int. The number of sampled from noise examples
        :return: Loss estimation with shape of [1]
            loss defined in Mikolov et al. Distributed Representations of Words and Phrases and their Compositionality
            papers.nips.cc/paper/5021-distributed-representations-of-words-and-phrases-and-their-compositionality.pdf
        """

        #use_cuda = self.in_embed.weight.is_cuda

        # use mask
        use_cuda = True
        loss_sum = 0.0
        sub_batch_sum = 0

        types = input_labels[:,0]
        [batch_size, window_size] = out_labels.size()
        window_size -= 1
        #print(window_size)
        #print(out_labels)
        #print(len(types))
        #map(lambda x: x)
        #hard encode 4 edge types

        for tp in xrange(len(self.edge_types)):
            type_u = self.edge_types[tp][0]
            type_v = self.edge_types[tp][1]
            #print(input_labels[t.LongTensor(np.where(types == t)),1])
            #indices = np.where(types == tp)[0]
            indices = t.nonzero(types == tp).squeeze()
            #print(indices)
            if len(indices) == 0:
                continue
            sub_batch_size = indices.size()[0]
            #print(sub_batch_size)
            input_tensor = t.index_select(input_labels[:,1], 0, indices).repeat(1, window_size).contiguous().view(-1)
            #print(t.index_select(out_labels, 0, tp_index)[:,1:])
            output_tensor = t.index_select(out_labels[:,1:], 0, indices).contiguous().view(-1)
            
        #input_tensor = input_labels.repeat(1, window_size).contiguous().view(-1)
        
        #output_tensor = out_labels[:,1:].contiguous().view(-1)

            if use_cuda:
                input_tensor = input_tensor.cuda()
                output_tensor = output_tensor.cuda()
            
            input = self.in_embed(Variable(input_tensor))
            output = self.out_embed(Variable(output_tensor))

            if self.weights is not None:
                noise_sample_count = sub_batch_size * window_size * num_sampled
                draw = self.sample(noise_sample_count)
                noise = draw.view(sub_batch_size * window_size, num_sampled)
            else:
                noise = Variable(t.Tensor(sub_batch_size * window_size, num_sampled).
                                 uniform_(0, self.type_offset[type_u+1] - self.type_offset[type_u] - 1).add_(self.type_offset[type_u]).long())
                cp_noise = Variable(t.Tensor(sub_batch_size * window_size, num_sampled).
                                 uniform_(0, self.type_offset[type_v+1] - self.type_offset[type_v] - 1).add_(self.type_offset[type_v]).long())

            if use_cuda:
                noise = noise.cuda()
                cp_noise = cp_noise.cuda()

            noise = self.in_embed(noise).neg()
            cp_noise = self.out_embed(cp_noise).neg()
            #print(input.size())
            #print(output.size())
            #print(self.edge_mapping[tp].size())
            
            log_target = self.edge_mapping[tp](input * output).sum(1).squeeze().sigmoid().log()
            #log_target = (input * output).sum(1).squeeze().sigmoid().log()

            '''[batch_size * window_size, num_sampled, embed_size] * [batch_size * window_size, embed_size, 1] ->
                [batch_size, num_sampled, 1] -> [batch_size] '''

            #squeeze replace size 1
            
            sum_log_sampled_u = ( self.edge_mapping[tp](noise*output.repeat(1, num_sampled).view(sub_batch_size,num_sampled,self.embed_size)).view(-1,self.embed_size)).sum(1).squeeze().sigmoid().log()
            sum_log_sampled_v = ( self.edge_mapping[tp](cp_noise*input.repeat(1, num_sampled).view(sub_batch_size,num_sampled,self.embed_size)).view(-1,self.embed_size)).sum(1).squeeze().sigmoid().log()
            
            #sum_log_sampled_u = t.bmm(noise, output.unsqueeze(2)).sigmoid().log().sum(1).squeeze()
            #sum_log_sampled_v = t.bmm(cp_noise, input.unsqueeze(2)).sigmoid().log().sum(1).squeeze()

            loss = 2 * log_target.sum() + sum_log_sampled_u.sum() + sum_log_sampled_v.sum() - \
            (input.mul(input).sum() + output.mul(output).sum() + noise.mul(noise).sum() + cp_noise.mul(cp_noise).sum() + sub_batch_size * self.edge_mapping[tp].weight.mul(self.edge_mapping[tp].weight).sum())
            #+ (input.mul(input).sum() + output.mul(output).sum() + noise.mul(noise).sum() + cp_noise.mul(cp_noise).sum() )
            #loss = log_target.sum() + sum_log_sampled_v.sum()
            #loss = log_target + sum_log_sampled_v
            #print(loss)
            #if np.isnan(loss.data.cpu().numpy()):
            #    print(tp)
                #print(input)
                #print(output)
            #    print(input.sum())
            #    print(output.sum())
            #    print(log_target.sum())
                #print(self.edge_mapping[tp].weight)
                #print(input_tensor)
                #print(output_tensor)
            loss_sum -= loss
            #sub_batch_sum += sub_batch_size
        #assert sub_batch_size == batch_size
        return loss_sum / (2 * batch_size)

    def input_embeddings(self):
        return self.in_embed.weight.data.cpu().numpy()