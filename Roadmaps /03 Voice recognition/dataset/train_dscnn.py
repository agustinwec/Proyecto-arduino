# train_dscnn.py
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
import numpy as np
from tqdm import tqdm

class DepthwiseSeparableConv(nn.Module):
    def __init__(self, in_ch, out_ch, kernel, stride=1, padding=0):
        super().__init__()
        self.depthwise = nn.Conv2d(in_ch, in_ch, kernel_size=kernel, stride=stride,
                                   padding=padding, groups=in_ch, bias=False)
        self.pointwise = nn.Conv2d(in_ch, out_ch, kernel_size=1, bias=False)
        self.bn = nn.BatchNorm2d(out_ch)
        self.act = nn.ReLU()

    def forward(self, x):
        x = self.depthwise(x)
        x = self.pointwise(x)
        x = self.bn(x)
        return self.act(x)

class DSCNN(nn.Module):
    def __init__(self, n_classes=2):
        super().__init__()
        # input: (B,1,40,49)
        self.conv1 = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=(3,3), stride=1, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU()
        )
        self.ds1 = DepthwiseSeparableConv(32,64,(3,3), padding=1)
        self.ds2 = DepthwiseSeparableConv(64,128,(3,3), padding=1)
        self.pool = nn.AdaptiveAvgPool2d((1,1))
        self.fc = nn.Linear(128, n_classes)

    def forward(self, x):
        x = self.conv1(x)
        x = self.ds1(x)
        x = self.ds2(x)
        x = self.pool(x).view(x.size(0), -1)
        return self.fc(x)

def load_data(npz='kws_dataset.npz', batch_size=32):
    d = np.load(npz, allow_pickle=True)
    X = d['X']  # (N,1,40,49)
    Y = d['Y']
    # shuffle+split
    idx = np.random.permutation(len(X))
    train_idx = idx[:int(0.8*len(X))]
    val_idx = idx[int(0.8*len(X)):]
    X_train, Y_train = X[train_idx], Y[train_idx]
    X_val, Y_val = X[val_idx], Y[val_idx]
    train_ds = TensorDataset(torch.tensor(X_train), torch.tensor(Y_train))
    val_ds = TensorDataset(torch.tensor(X_val), torch.tensor(Y_val))
    return DataLoader(train_ds, batch_size=batch_size, shuffle=True), DataLoader(val_ds, batch_size=batch_size)

def train(epochs=30):
    train_loader, val_loader = load_data()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = DSCNN(n_classes=2).to(device)
    opt = optim.Adam(model.parameters(), lr=1e-3)
    crit = nn.CrossEntropyLoss()
    for e in range(epochs):
        model.train()
        loop = tqdm(train_loader)
        for xb,yb in loop:
            xb = xb.to(device).float()
            yb = yb.to(device)
            opt.zero_grad()
            out = model(xb)
            loss = crit(out, yb)
            loss.backward()
            opt.step()
            loop.set_description(f"Epoch {e} Loss {loss.item():.4f}")
        # eval
        model.eval()
        correct=0; total=0
        with torch.no_grad():
            for xb,yb in val_loader:
                xb=xb.to(device).float(); yb=yb.to(device)
                out = model(xb)
                pred = out.argmax(dim=1)
                correct += (pred==yb).sum().item()
                total += len(yb)
        print(f"Val acc: {correct/total:.3f}")
    torch.save(model.state_dict(), 'dscnn_kws.pth')
    print('Saved dscnn_kws.pth')

if __name__=='__main__':
    train(epochs=80)
