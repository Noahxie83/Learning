import torch
import torch.nn as nn

# X = torch.tensor([1, 2, 3, 4], dtype=torch.float32)
# Y = torch.tensor([2, 4, 6, 8], dtype=torch.float32)
X = torch.tensor([[1], [2], [3], [4]], dtype=torch.float32)
Y = torch.tensor([[2], [4], [6], [8]], dtype=torch.float32)

X_test = torch.tensor([5], dtype=torch.float32)
n_samples, n_features = X.shape
print(n_samples, n_features)

# w = torch.tensor(0.0, dtype=torch.float32, requires_grad=True)
# def forward(x):
#     return w*x
input_size = n_features
output_size = n_features
model = nn.Linear(input_size, output_size)

# def loss(y, y_hat):
#     return ((y_hat-y)**2).mean()
loss = nn.MSELoss()

print(f'Prediction before training: f{5} = {model(X_test).item():.3f}')

learning_rate = 0.01
n_iters = 100

optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
for epoch in range(n_iters):
    y_hat = model(X)
    l = loss(Y,y_hat)
    l.backward()
    
    # with torch.no_grad():
    #     w -= learning_rate*w.grad
    optimizer.step()
    
    # w.grad.zero_()
    optimizer.zero_grad()
    if epoch %10 == 0:
        [w, b] = model.parameters()
        print(f'epoch {epoch+1}: w = {w[0][0].item():.3f}, loss = {l:.8f}')
print(f'Prediction after training: f{5} = {model(X_test).item():.3f}')