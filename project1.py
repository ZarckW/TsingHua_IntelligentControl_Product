import torch
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt
import numpy as np
import math
import func 
#定义网络
class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv1d(1,4,kernel_size=2),
            nn.BatchNorm1d(4),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2))
        self.layer2 = nn.Sequential(
            nn.Conv1d(4, 16, kernel_size=2),
            nn.BatchNorm1d(16),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2))
        self.layer3 = nn.Sequential(
            nn.Conv1d(16, 16, kernel_size=2),
            nn.BatchNorm1d(16),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2))
        self.layer4 = nn.Sequential(
            nn.Conv1d(16, 1, kernel_size=2),
            nn.BatchNorm1d(1),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2))
        self.fc0= nn.Linear(1,500)
        self.fc1= nn.Linear(30,1)
    def forward(self, x):
        out = self.fc0(x)
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = self.fc1(out)
        return out
#载入网络
net=Net()
net.load_state_dict(torch.load('Mynet.pkl'))
optimizer = torch.optim.SGD(net.parameters(), lr=0.02)
loss_func = torch.nn.MSELoss() 
#生成测试数据集
t=np.random.rand(400)*1400
t=np.sort(t)
n=np.size(t)

ans=func.NARMA(t,n)
ans=torch.from_numpy(ans).float()
ans=ans.reshape(400,1,1)
t=torch.from_numpy(t).float()
t=t.reshape(400,1,1)

#dataset=[torch.from_numpy(t).float(),torch.from_numpy(ans).float()]

#测试网络
net.eval()
test_out=net(t)
loss = loss_func(test_out,ans)
print(loss)

