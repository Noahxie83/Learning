import torch
from torch import nn
from d2l import torch as d2l
import matplotlib.pyplot as plt

batch_size = 256
train_iter, test_iter = d2l.load_data_fashion_mnist(batch_size)

num_inputs, num_outputs, num_hiddens = 28*28, 10, 256
W1 = nn.Parameter(torch.randn(num_inputs, num_hiddens, requires_grad=True)*0.01)
# print(W1)
b1 = nn.Parameter(torch.zeros(num_hiddens))
W2 = nn.Parameter(torch.randn(num_hiddens, num_outputs, requires_grad=True)*0.01)
b2 = nn.Parameter(torch.zeros(num_outputs))
para_list = [W1, b1, W2, b2]

def ReLU(X):
  tmp = torch.zeros_like(X)  
  return torch.max(tmp, X)

def net(X):
    X = X.reshape((-1, num_inputs))
    Hidden = ReLU(X@W1 + b1)
    return Hidden@W2 + b2

loss = nn.CrossEntropyLoss() 

num_epochs, lr = 10, 0.1
optimizer = torch.optim.SGD(para_list, lr=lr)
d2l.train_ch3(net, train_iter, test_iter, loss, num_epochs, optimizer)
# def train_ch3(net, train_iter, test_iter, loss, num_epochs, updater):
d2l.predict_ch3(net, test_iter)
# def predict_ch3(net, test_iter, n=6)

plt.show()