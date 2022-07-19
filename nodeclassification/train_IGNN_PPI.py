from __future__ import division
from __future__ import print_function

import os
import os.path as osp
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
import time
import argparse
import numpy as np

import torch
import torch.nn.functional as F
import torch.optim as optim
from torch_geometric.datasets import PPI
from torch_geometric.data import DataLoader
from sklearn.metrics import f1_score


from utils import load_citation, accuracy, clip_gradient, l_1_penalty
from models_PPI import IGNN

# Training settings
parser = argparse.ArgumentParser()
parser.add_argument('--no-cuda', action='store_true', default=False,
                    help='Disables CUDA training.')
parser.add_argument('--fastmode', action='store_true', default=False,
                    help='Validate during training pass.')
parser.add_argument('--seed', type=int, default=42, help='Random seed.')
parser.add_argument('--epochs', type=int, default=1000,
                    help='Number of epochs to train.')
parser.add_argument('--lr', type=float, default=0.01,
                    help='Initial learning rate.')
parser.add_argument('--weight_decay', type=float, default=0,
                    help='Weight decay (L2 loss on parameters).')
parser.add_argument('--hidden', type=int, default=256,
                    help='Number of hidden units.')
parser.add_argument('--dropout', type=float, default=0.5,
                    help='Dropout rate (1 - keep probability).')
parser.add_argument('--kappa', type=float, default=0.98,
                    help='Projection parameter. ||W|| <= kappa/lpf(A)')
parser.add_argument('--dataset', type=str, default="cora",
                        help='Dataset to use.')
parser.add_argument('--feature', type=str, default="mul",
                    choices=['mul', 'cat', 'adj'],
                    help='feature-type')
parser.add_argument('--normalization', type=str, default='AugNormAdj',
                   choices=['AugNormAdj'],
                   help='Normalization method for the adjacency matrix.')
parser.add_argument('--degree', type=int, default=2,
                    help='degree of the approximation.')
parser.add_argument('--per', type=int, default=-1,
                    help='Number of each nodes so as to balance.')
parser.add_argument('--experiment', type=str, default="base-experiment",
                    help='feature-type')
args = parser.parse_args()
args.cuda = not args.no_cuda and torch.cuda.is_available()


np.random.seed(args.seed)
torch.manual_seed(args.seed)
if args.cuda:
    torch.cuda.manual_seed(args.seed)

# Load data
path = osp.join(osp.dirname(osp.realpath(__file__)), 'data', 'PPI')
train_dataset = PPI(path, split='train')
val_dataset = PPI(path, split='val')
test_dataset = PPI(path, split='test')
train_loader = DataLoader(train_dataset, batch_size=1, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=2, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=2, shuffle=False)

# Model and optimizer
device = torch.device('cuda' if args.cuda else 'cpu')
model = IGNN(nfeat=train_dataset.num_features,
            nhid=args.hidden,
            nclass=train_dataset.num_classes,
            num_node = None,
            dropout=args.dropout,
            kappa=args.kappa).to(device)

loss_op = torch.nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.005)


def train():
    model.train()

    total_loss = 0
    for data in train_loader:
        num_graphs = data.num_graphs
        data.batch = None
        data = data.to(device)
        optimizer.zero_grad()
        if data.edge_attr is None:
            edge_weight = torch.ones((data.edge_index.size(1), ), dtype=data.x.dtype, device=data.edge_index.device)
        adj = torch.sparse.FloatTensor(data.edge_index, edge_weight, torch.Size([data.num_nodes, data.num_nodes]))
        loss = loss_op(model(data.x.T, adj), data.y)
        total_loss += loss.item() * num_graphs
        loss.backward()
        optimizer.step()
    return total_loss / len(train_loader.dataset)


def test(loader):
    model.eval()

    ys, preds = [], []
    for data in loader:
        ys.append(data.y)
        if data.edge_attr is None:
            edge_weight = torch.ones((data.edge_index.size(1), ), dtype=data.x.dtype, device=data.edge_index.device)
        adj = torch.sparse.FloatTensor(data.edge_index, edge_weight, torch.Size([data.num_nodes, data.num_nodes]))
        with torch.no_grad():
            out = model(data.x.T.to(device), adj.to(device))
        preds.append((out > 0).float().cpu())

    y, pred = torch.cat(ys, dim=0).numpy(), torch.cat(preds, dim=0).numpy()
    return f1_score(y, pred, average='micro') if pred.sum() > 0 else 0

best_f1 = 0
best_epoch = 0
for epoch in range(1, int(args.epochs) + 1):
    loss = train()
    val_f1 = test(val_loader)
    test_f1 = test(test_loader)
    if test_f1 > best_f1:
        best_f1 = test_f1
        best_epoch = epoch
    print('Epoch: {:02d}, Loss: {:.4f}, Val: {:.4f}, Test: {:.4f}'.format(
        epoch, loss, val_f1, test_f1))

print('Best f1 micro is: {} at epoch {}'.format(best_f1, best_epoch))

