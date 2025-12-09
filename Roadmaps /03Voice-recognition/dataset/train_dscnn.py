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
        # bloque 1
        self.ds1 = DepthwiseSeparableConv(32, 64, (3,3), padding=1)
        # bloque 2
        self.ds2 = DepthwiseSeparableConv(64, 128, (3,3), padding=1)
        # bloque 3 extra (más capacidad)
        self.ds3 = DepthwiseSeparableConv(128, 128, (3,3), padding=1)

        self.pool = nn.AdaptiveAvgPool2d((1,1))
        self.dropout = nn.Dropout(0.3)
        self.fc = nn.Linear(128, n_classes)

    def forward(self, x):
        x = self.conv1(x)
        x = self.ds1(x)
        x = self.ds2(x)
        x = self.ds3(x)
        x = self.pool(x).view(x.size(0), -1)
        x = self.dropout(x)
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
    train_ds = TensorDataset(
        torch.tensor(X_train, dtype=torch.float32),
        torch.tensor(Y_train, dtype=torch.long)
    )
    val_ds = TensorDataset(
        torch.tensor(X_val, dtype=torch.float32),
        torch.tensor(Y_val, dtype=torch.long)
    )
    return DataLoader(train_ds, batch_size=batch_size, shuffle=True), DataLoader(val_ds, batch_size=batch_size)

def train(epochs=30):
    train_loader, val_loader = load_data()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = DSCNN(n_classes=2).to(device)
    opt = optim.Adam(model.parameters(), lr=5e-4)
    crit = nn.CrossEntropyLoss()

    best_acc = 0.0

    for e in range(epochs):
        model.train()
        loop = tqdm(train_loader)
        for xb, yb in loop:
            xb = xb.to(device).float()
            yb = yb.to(device)
            opt.zero_grad()
            out = model(xb)
            loss = crit(out, yb)
            loss.backward()
            opt.step()
            loop.set_description(f"Epoch {e} Loss {loss.item():.4f}")

        # ==== eval en TRAIN ====
        model.eval()
        train_correct = 0
        train_total = 0
        with torch.no_grad():
            for xb, yb in train_loader:
                xb = xb.to(device).float()
                yb = yb.to(device)
                out = model(xb)
                pred = out.argmax(dim=1)
                train_correct += (pred == yb).sum().item()
                train_total += len(yb)
        train_acc = train_correct / train_total

        # ==== eval en VAL (como ya tenés) ====
        val_correct = 0
        val_total = 0
        with torch.no_grad():
            for xb, yb in val_loader:
                xb = xb.to(device).float()
                yb = yb.to(device)
                out = model(xb)
                pred = out.argmax(dim=1)
                val_correct += (pred == yb).sum().item()
                val_total += len(yb)
        val_acc = val_correct / val_total

        print(f"Epoch {e} | train acc: {train_acc:.3f} | val acc: {val_acc:.3f}")

        # guardar solo el mejor
        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(), 'dscnn_kws.pth')
            print(f"✅ Nuevo mejor modelo guardado (acc={best_acc:.3f})")

    print(f"Entrenamiento terminado. Mejor val acc = {best_acc:.3f}")

if __name__=='__main__':
    train(epochs=50)