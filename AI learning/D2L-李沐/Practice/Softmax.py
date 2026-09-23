import torch
import torch.nn as nn

loss = nn.CrossEntropyLoss()

Y = torch.tensor([2, 0, 1])
Y_pred_good = torch.tensor([[0.1, 1.0, 2.1], 
                            [2.0, 1.0, 0.1], 
                            [0.1, 3.0, 0.1]])
Y_pred_bad = torch.tensor([[2.1, 1.0, 0.1], 
                            [0.1, 1.0, 2.1], 
                            [0.1, 3.0, 0.1]])

l1 = loss(Y_pred_good, Y)
l2 = loss(Y_pred_bad, Y)

print(l1.item())
print(l2.item())

_, prediction1 = torch.max(Y_pred_good, 1)
_, prediction2 = torch.max(Y_pred_bad, 1)
print(prediction1)
print(prediction2)