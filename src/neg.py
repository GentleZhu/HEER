import torch as t
import torch.nn as nn
from torch.autograd import Variable
from torch.nn import Parameter
import numpy as np
import cPickle
import utils


class NEG_loss(nn.Module):
    def __init__(self, type_offset, node_types, edge_types, embed_size, pre_train_path, graph_name = '', mode=1, weight_decay=0.001, directed=False):
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
        self.directed = directed
        self.mode = mode
        self.weight_decay = weight_decay
        for tp in node_types:
            self.type_offset.append(type_offset[tp])

        self.edge_types = edge_types
        self.embed_size = embed_size
        self.in_embed = nn.Embedding(self.num_classes, self.embed_size, sparse=True)

        self.edge_mapping = nn.ModuleList()
        self.out_embed = nn.Embedding(self.num_classes, self.embed_size, sparse=True)

        #self.add_module('in_emb', self.in_embed)
        #self.add_module('out_emb', self.out_embed)
        #self.add_module('edge_map', self.edge_mapping)

        self.out_embed.weight = Parameter(t.FloatTensor(self.num_classes, self.embed_size).uniform_(-1, 1).cuda())
        self.in_embed.weight = Parameter(t.FloatTensor(self.num_classes, self.embed_size).uniform_(-1, 1).cuda())

        if len(pre_train_path) > 0:
            '''
            in_mapping = cPickle.load(open('/shared/data/qiz3/data/' + graph_name +'in_mapping.p'))
            with open(pre_train_path, 'r') as INPUT:
                INPUT.readline()
                for line in INPUT:
                    node = line.strip().split(' ')
                    _type, _id = node[0].split(':')
                    _index = in_mapping[_type][_id] + self.type_offset[node_types.index(_type)]
                    self.out_embed.weight.data[_index, :] = t.FloatTensor(map(lambda x:float(x), node[1:]))
                    self.in_embed.weight.data[_index, :] = t.FloatTensor(map(lambda x:float(x), node[1:]))
            '''
            self.in_embed.weight.data.copy_(t.from_numpy(pre_train_path))
            self.out_embed.weight.data.copy_(t.from_numpy(pre_train_path))
            self.in_embed.weight.data.div_(10)
            self.out_embed.weight.data.div_(10)
            #self.out_embed.weight.data.renorm_(p=2, dim=0, maxnorm=2)
            #self.edge_mapping.append(nn.Linear(self.embed_size, self.embed_size, bias=False).cuda())
        
        if self.mode > 0: 
            for tp in edge_types:
                self.edge_mapping.append(self.genMappingLayer(self.mode))
        
        self.type_offset.append(type_offset['sum'])
        print(self.type_offset)
        #print(self.type_offset)

    def genMappingLayer(self, mode):
        _layer = None
        if mode != 2:
            _layer = utils.DiagLinear(self.embed_size).cuda()
            _layer.weight = Parameter(t.FloatTensor(self.embed_size).fill_(1.0).cuda())
        elif mode == 2:
            _layer = utils.SymmLinear(self.embed_size).cuda()
            #_layer.weight = Parameter(t.FloatTensor(self.embed_size * self.embed_size).fill_(1.0).cuda())
            _layer.weight = Parameter(t.eye(self.embed_size).view(-1, self.embed_size ** 2).cuda())
        return _layer


    def edge_rep(self, input_a, input_b, tp):
        #mode 1: element-wise
        #mode 2: outer-product
        #mode 3: deduction
        #mode 4: addition
        if self.mode == 1:
            return self.edge_mapping[tp](input_a * input_b)
        elif self.mode == 2:
            return self.edge_mapping[tp](t.bmm(input_a.unsqueeze(2), input_b.unsqueeze(1)).view(-1, self.embed_size ** 2) + 
                t.bmm(input_b.unsqueeze(2), input_a.unsqueeze(1)).view(-1, self.embed_size ** 2) )
        elif self.mode == 3:
            return self.edge_mapping[tp]((input_a - input_b) ** 2)
        elif self.mode == 4:
            return self.edge_mapping[tp]((input_a + input_b) ** 2)
        else:
            return input_a * input_b
    
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
        #sub_loss = []
        loss_sum = 0.0
        pure_loss = 0.0

        types = input_labels[:,0]
        [batch_size, window_size] = out_labels.size()
        window_size -= 1
        #sub_batches = []
        for tp in xrange(len(self.edge_types)):
            #if tp == 11:
            #    continue
            loss = 0.0
            reg_loss = 0.0
            type_u = self.edge_types[tp][0]
            type_v = self.edge_types[tp][1]
            #print(input_labels[t.LongTensor(np.where(types == t)),1])
            #indices = np.where(types == tp)[0]
            indices = t.nonzero(types == tp).squeeze()
            #print(indices)
            if len(indices) == 0:
                continue
            sub_batch_size = indices.size()[0]
            #sub_batches.append(sub_batch_size)

            input_tensor = t.index_select(input_labels[:,1], 0, indices).repeat(1, window_size).contiguous().view(-1)
            output_tensor = t.index_select(out_labels[:,1:], 0, indices).contiguous().view(-1)

            if use_cuda:
                input_tensor = input_tensor.cuda()
                output_tensor = output_tensor.cuda()

            input = self.in_embed(Variable(input_tensor))
            output = self.out_embed(Variable(output_tensor))

            _noise = Variable(t.Tensor(sub_batch_size * window_size, num_sampled).
                             uniform_(0, self.type_offset[type_u+1] - self.type_offset[type_u] - 1).add_(self.type_offset[type_u]).long())
            _cp_noise = Variable(t.Tensor(sub_batch_size * window_size, num_sampled).
                             uniform_(0, self.type_offset[type_v+1] - self.type_offset[type_v] - 1).add_(self.type_offset[type_v]).long())

            if use_cuda:
                _noise = _noise.cuda()
                _cp_noise = _cp_noise.cuda()

            noise = self.in_embed(_noise).neg()
            cp_noise = self.out_embed(_cp_noise).neg()

            

            sum_log_sampled_u = self.edge_rep(noise.view(-1, self.embed_size), output.repeat(1, num_sampled).view(-1,self.embed_size), tp).sum(1).squeeze().clamp(min=-6, max=6).sigmoid().log()
            sum_log_sampled_v = self.edge_rep(cp_noise.view(-1, self.embed_size), input.repeat(1, num_sampled).view(-1,self.embed_size), tp).sum(1).squeeze().clamp(min=-6, max=6).sigmoid().log()

            if not self.directed and type_u != type_v:
                u_input = self.in_embed(Variable(output_tensor))
                u_output = self.out_embed(Variable(input_tensor))
                u_noise = self.in_embed(_cp_noise).neg()
                u_cp_noise = self.out_embed(_noise).neg()
                log_target = self.edge_rep(input, u_input, tp).sum(1).squeeze().clamp(min=-6, max=6).sigmoid().log()
                reverse_log_target = self.edge_rep(output , u_output, tp).sum(1).squeeze().clamp(min=-6, max=6).sigmoid().log()
                reverse_sum_log_sampled_u = self.edge_rep(u_noise.view(-1, self.embed_size), u_output.repeat(1, num_sampled).view(-1,self.embed_size), tp).sum(1).squeeze().clamp(min=-6, max=6).sigmoid().log()
                reverse_sum_log_sampled_v = self.edge_rep(u_cp_noise.view(-1, self.embed_size), u_input.repeat(1, num_sampled).view(-1,self.embed_size), tp).sum(1).squeeze().clamp(min=-6, max=6).sigmoid().log()
                loss = log_target.sum() + reverse_log_target.sum() + (sum_log_sampled_u.sum() + sum_log_sampled_v.sum() + reverse_sum_log_sampled_u.sum() + reverse_sum_log_sampled_v.sum()) / 2
                reg_loss = (input.mul(input).sum() + output.mul(output).sum() + noise.mul(noise).sum() + cp_noise.mul(cp_noise).sum() + 
                u_input.mul(u_input).sum() + u_output.mul(u_output).sum() + u_noise.mul(u_noise).sum() + u_cp_noise.mul(u_cp_noise).sum()) / 2
            else:
                log_target = self.edge_rep(input, output, tp).sum(1).squeeze().clamp(min=-6, max=6).sigmoid().log()
                loss = 2 * log_target.sum() + sum_log_sampled_u.sum() + sum_log_sampled_v.sum()
                reg_loss = input.mul(input).sum() + output.mul(output).sum() + noise.mul(noise).sum() + cp_noise.mul(cp_noise).sum()

            #if tp != 1:


            '''[batch_size * window_size, num_sampled, embed_size] * [batch_size * window_size, embed_size, 1] ->
                [batch_size, num_sampled, 1] -> [batch_size] '''

            #squeeze replace size 1
            
            #sum_log_sampled_u = ( self.edge_mapping[tp](noise*output.repeat(1, num_sampled).view(sub_batch_size,num_sampled,self.embed_size)).view(-1,self.embed_size)).sum(1).squeeze().sigmoid().log()
            #temp = self.edge_rep(noise*output.repeat(1, num_sampled).view(sub_batch_size,num_sampled,self.embed_size), tp).view(-1,self.embed_size).sum(1).sigmoid()

            
            #sum_log_sampled_u = t.bmm(noise, output.unsqueeze(2)).sigmoid().log().sum(1).squeeze()
            #sum_log_sampled_v = t.bmm(cp_noise, input.unsqueeze(2)).sigmoid().log().sum(1).squeeze()

             #+ input.norm(p=2, dim=1, keepdim=True).sum() + output.norm(p=2, dim=1, keepdim=True).sum() + noise.norm(p=2, dim=1, keepdim=True).sum() + cp_noise.norm(p=2, dim=1, keepdim=True).sum() + self.edge_mapping[tp].weight.norm(p=2, keepdim=True).sum()
            
            edge_reg_loss = 0.0
            if self.mode > 0:
                edge_reg_loss += self.edge_mapping[tp].weight.mul(self.edge_mapping[tp].weight).sum()
            reg_loss += sub_batch_size * edge_reg_loss
            #loss = log_target.sum() + sum_log_sampled_v.sum()
            #loss = log_target + sum_log_sampled_v
            #print(loss)
            #loss_sum -= (loss - self.weight_decay * reg_loss)
            #sub_loss.append((-loss + self.weight_decay * reg_loss) / (2 * sub_batch_size))
            loss_sum -= (loss - self.weight_decay * reg_loss)
            pure_loss -= loss
            #print(loss, reg_loss)
            #print(sub_batch_size)
            #print('type :', tp, sub_batch_size, sum_log_sampled_u.sum(), sum_log_sampled_v.sum(), noise.mul(noise).sum(), cp_noise.mul(cp_noise).sum())
            #print('Type is ', tp)
            #print(input.norm(p=2, dim=1, keepdim=True).sum())
            #print(output.norm(p=2, dim=1, keepdim=True).sum())
            #if np.isnan(loss_sum[-1].data.cpu().numpy()):
            #print('Type :', tp, temp.data.cpu().numpy().tolist())
            #print(self.edge_mapping[tp].weight.data.cpu().numpy().tolist())
        #print(sub_batch_size)
        #assert sum(sub_batches) == batch_size
        #return sub_loss, loss_sum
        return loss_sum / (2 * batch_size), pure_loss / (2 * batch_size)

    def predict(self, inputs, outputs, tp, directed = False):
        use_cuda = True
        if use_cuda:
            inputs = inputs.cuda()
            outputs = outputs.cuda()

        input = self.in_embed(Variable(inputs))
        output = self.out_embed(Variable(outputs))

        if not directed:
            u_input = self.in_embed(Variable(outputs))
            u_output = self.out_embed(Variable(inputs))
            log_target = self.edge_rep(input, u_input, tp).sum(1).squeeze().sigmoid() + self.edge_rep(output, u_output, tp).sum(1).squeeze().sigmoid()
            log_target /= 2
        else:
            log_target = self.edge_rep(input, output, tp).sum(1).squeeze().sigmoid()
        #log_target = (input * output).sum(1).squeeze().sigmoid()
        
        return log_target.data.cpu().numpy().tolist()

    def input_embeddings(self):
        return self.in_embed.weight.data.cpu().numpy()
