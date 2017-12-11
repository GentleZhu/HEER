import torch
import torch.nn as nn
from torch.nn import Parameter

class DiagLinear(nn.Module):
    def __init__(self, input_features):
        super(DiagLinear, self).__init__()
        self.input_features = input_features

        # nn.Parameter is a special kind of Variable, that will get
        # automatically registered as Module's parameter once it's assigned
        # as an attribute. Parameters and buffers need to be registered, or
        # they won't appear in .parameters() (doesn't apply to buffers), and
        # won't be converted when e.g. .cuda() is called. You can use
        # .register_buffer() to register buffers.
        # nn.Parameters can never be volatile and, different than Variables,
        # they require gradients by default.
        self.weight = nn.Parameter(torch.Tensor(input_features))

        # Not a very smart way to initialize weights
        self.weight.data.uniform_(-0.1, 0.1)

    def forward(self, input):
        # See the autograd section for explanation of what happens here.
        return input * self.weight