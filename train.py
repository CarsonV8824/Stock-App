import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

from tensors import training_tensors
from model import StockMLP

BATCH_SIZE = 64
LEARNING_RATE = 0.001
LEARNING_DECAY = 1e-5
NUM_EPOCHS = 121
CHECKPOINT_INTERVAL = 15
VALIDATION_SPLIT = 0.2
MODEL_PATH = "model.pth"

def train():
    device = torch.device("xpu")

    X_train, y_train, X_val, y_val = training_tensors(VALIDATION_SPLIT)
    X_train = X_train.to(device)
    y_train = y_train.to(device)
    X_val = X_val.to(device)
    y_val = y_val.to(device)

    dataset = TensorDataset(X_train, y_train)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
    model = StockMLP(input_size=X_train.shape[1]).to(device)
    loss_fn = nn.L1Loss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE, weight_decay=LEARNING_DECAY)

    scores = dict()
    scores["epchos"] = []
    scores["train_loss"] = []
    scores["val_loss"] = []
    for epoch in range(NUM_EPOCHS):
        model.train()
        for X_batch, y_batch in dataloader:
            predictions = model(X_batch).squeeze()
            loss = loss_fn(predictions, y_batch)

            optimizer.zero_grad()
                
            loss.backward()
            optimizer.step()

        if epoch % CHECKPOINT_INTERVAL == 0:
            model.eval()
            with torch.no_grad():
                train_predictions = model(X_train).squeeze()
                train_loss = loss_fn(train_predictions, y_train)
                val_predictions = model(X_val).squeeze()
                val_loss = loss_fn(val_predictions, y_val)
            print(f"epoch {epoch}, train_loss = {train_loss.item()}, val_loss = {val_loss.item()}")
            scores["epchos"].append(epoch)
            scores["train_loss"].append(train_loss.item())
            scores["val_loss"].append(val_loss.item())
        print(epoch)

    torch.save(model.state_dict(), MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

    temp = pd.DataFrame(scores)
    sns.regplot(x=temp["epchos"], y=temp["train_loss"], label="train")
    
    plt.title("Training vs validation loss by epoch")
    plt.xticks(range(int(temp["epchos"].min()), int(temp["epchos"].max()) + 1, CHECKPOINT_INTERVAL))
    plt.legend()
    plt.show()

    sns.regplot(x=temp["epchos"], y=temp["val_loss"], label="validation")
    plt.title("Training vs validation loss by epoch")
    plt.xticks(range(int(temp["epchos"].min()), int(temp["epchos"].max()) + 1, CHECKPOINT_INTERVAL))
    plt.legend()
    plt.show()

if __name__ == "__main__":
    train()
