import torch
import torch.nn as nn

class Transformador( nn.Module ):
    def __init__(self, n_inputs, n_hidden):
        super().__init__()
        self.layer1 = nn.Linear(n_inputs, n_hidden)
        self.relu = nn.ReLU()
        self.layer2 = nn.Linear(n_hidden, n_inputs)


    def forward(self, x):
        h = self.layer1(x)
        y = self.relu(h)
        z = self.layer2(y)
        return z, h
    