import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import os

# CONFIGURATION
DATA_DIR = r'C:\Users\magic\Downloads\erickson_data'
INPUT_CSV = os.path.join(DATA_DIR, 'erickson_sequences_with_submacros.csv')
SEQ_LENGTH = 5 
BATCH_SIZE = 64
EPOCHS = 50
LEARNING_RATE = 0.005
EMBEDDING_DIM = 32
HIDDEN_DIM = 64

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

print("Loading sub_macro data...")
df = pd.read_csv(INPUT_CSV)
df = df.sort_values(by=['script_id', 'turn_no'])

labels = df['sub_macro'].tolist()

# Build Vocabulary
vocab = list(set(labels))
vocab.sort()
vocab_size = len(vocab)
word_to_ix = {word: i for i, word in enumerate(vocab)}
ix_to_word = {i: word for i, word in enumerate(vocab)}

print(f"Vocabulary Size: {vocab_size}")
print(f"Vocab: {vocab}")

# Create Sequences
sequences = []
targets = []

for name, group in df.groupby('script_id'):
    macros = group['sub_macro'].tolist()
    indices = [word_to_ix[m] for m in macros]
    
    for i in range(len(indices) - SEQ_LENGTH):
        seq = indices[i:i + SEQ_LENGTH]
        target = indices[i + SEQ_LENGTH]
        sequences.append(seq)
        targets.append(target)

class EricksonContextDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.tensor(X, dtype=torch.long)
        self.y = torch.tensor(y, dtype=torch.long)
        
    def __len__(self):
        return len(self.X)
    
    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

dataset = EricksonContextDataset(sequences, targets)
train_size = int(0.9 * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size], generator=torch.Generator().manual_seed(42))

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)

print(f"Total sequences generated: {len(dataset)}")

class DeepEricksonLSTM(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim):
        super(DeepEricksonLSTM, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True, num_layers=2, dropout=0.3)
        self.fc = nn.Linear(hidden_dim, vocab_size)
        
    def forward(self, x):
        embedded = self.embedding(x)
        lstm_out, _ = self.lstm(embedded)
        out = self.fc(lstm_out[:, -1, :])
        return out

model = DeepEricksonLSTM(vocab_size, EMBEDDING_DIM, HIDDEN_DIM).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

print("Starting training...")
best_val_loss = float('inf')

for epoch in range(EPOCHS):
    model.train()
    total_loss = 0
    for X_batch, y_batch in train_loader:
        X_batch, y_batch = X_batch.to(device), y_batch.to(device)
        
        optimizer.zero_grad()
        predictions = model(X_batch)
        loss = criterion(predictions, y_batch)
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
        
    model.eval()
    val_loss = 0
    with torch.no_grad():
        for X_val, y_val in val_loader:
            X_val, y_val = X_val.to(device), y_val.to(device)
            val_preds = model(X_val)
            v_loss = criterion(val_preds, y_val)
            val_loss += v_loss.item()
            
    avg_train_loss = total_loss / len(train_loader)
    avg_val_loss = val_loss / len(val_loader)
    
    if (epoch + 1) % 5 == 0:
        print(f"Epoch {epoch+1}/{EPOCHS} | Train Loss: {avg_train_loss:.4f} | Val Loss: {avg_val_loss:.4f}")
        
    if avg_val_loss < best_val_loss:
        best_val_loss = avg_val_loss
        torch.save(model.state_dict(), os.path.join(DATA_DIR, 'erickson_other_lstm.pth'))

print("Training finished! Best model saved.")

def test_prediction(model, context_words):
    model.eval()
    model.to('cpu')
    with torch.no_grad():
        indices = [word_to_ix[w] for w in context_words]
        tensor_input = torch.tensor([indices], dtype=torch.long)
        output = model(tensor_input)
        probs = torch.nn.functional.softmax(output[0], dim=0).numpy()
        top_indices = probs.argsort()[-3:][::-1]
        
        print(f"\n[Test Context]: {' -> '.join(context_words)}")
        print("  => [Predicted Next]:")
        for idx in top_indices:
            print(f"     - {ix_to_word[idx]}: {probs[idx]*100:.1f}%")

print("\n--- Testing Dark Matter Prediction ---")
model.load_state_dict(torch.load(os.path.join(DATA_DIR, 'erickson_other_lstm.pth'), weights_only=True))

# Scenario A: Pacing followed by an Inquiry
test_prediction(model, ["PACING", "PACING", "PACING", "OTHER_UNKNOWN", "OTHER_INQUIRY"])
# Scenario B: Purely dissociative trance building
test_prediction(model, ["CONFUSION", "OTHER_DISSOCIATION", "OTHER_DISSOCIATION", "OTHER_TIME_AMNESIA", "OTHER_CUE_PROMPT"])
