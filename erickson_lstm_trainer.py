import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import numpy as np
import json
import os
from sklearn.model_selection import train_test_split

# 1. Configuration
WINDOW_SIZE = 5
EMBEDDING_DIM = 64
HIDDEN_DIM = 128
BATCH_SIZE = 32
EPOCHS = 20
LEARNING_RATE = 0.001

class EricksonDataset(Dataset):
    def __init__(self, sequences, targets):
        self.sequences = torch.tensor(sequences, dtype=torch.long)
        self.targets = torch.tensor(targets, dtype=torch.long)
        
    def __len__(self):
        return len(self.targets)
    
    def __getitem__(self, idx):
        return self.sequences[idx], self.targets[idx]

class EricksonLSTM(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim):
        super(EricksonLSTM, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True, num_layers=2, dropout=0.2)
        self.fc = nn.Linear(hidden_dim, output_dim)
        
    def forward(self, x):
        # x: [batch_size, seq_len]
        embeds = self.embedding(x) # [batch_size, seq_len, embed_dim]
        lstm_out, _ = self.lstm(embeds) # [batch_size, seq_len, hidden_dim]
        # Use the last time step's output
        last_out = lstm_out[:, -1, :]
        out = self.fc(last_out)
        return out

def train_model():
    print("Preparing data for LSTM...")
    # Load combined data
    csv_path = 'erickson_sequences_with_submacros.csv'
    df = pd.read_csv(csv_path)
    
    # Get unique patterns and create vocabulary
    all_patterns = sorted(df['pattern_id'].unique().tolist())
    pattern_to_idx = {p: i for i, p in enumerate(all_patterns)}
    idx_to_pattern = {i: p for p, i in pattern_to_idx.items()}
    vocab_size = len(all_patterns)
    
    # Save vocabulary
    with open('pattern_vocab.json', 'w') as f:
        json.dump(pattern_to_idx, f)
    
    sequences = []
    targets = []
    
    # Group by script to build sequences
    for script_id, group in df.groupby('script_id'):
        p_indices = [pattern_to_idx[p] for p in group.sort_values('turn_no')['pattern_id']]
        
        for i in range(WINDOW_SIZE, len(p_indices)):
            sequences.append(p_indices[i-WINDOW_SIZE:i])
            targets.append(p_indices[i])
            
    print(f"Total sequences generated: {len(sequences)}")
    
    # Split into train and test
    X_train, X_test, y_train, y_test = train_test_split(sequences, targets, test_size=0.2, random_state=42)
    
    train_dataset = EricksonDataset(X_train, y_train)
    test_dataset = EricksonDataset(X_test, y_test)
    
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)
    
    # Initialize Model
    model = EricksonLSTM(vocab_size, EMBEDDING_DIM, HIDDEN_DIM, vocab_size)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
    
    print(f"Starting training for {EPOCHS} epochs...")
    for epoch in range(EPOCHS):
        model.train()
        total_loss = 0
        for batch_seq, batch_target in train_loader:
            optimizer.zero_grad()
            output = model(batch_seq)
            loss = criterion(output, batch_target)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
            
        # Validation
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for batch_seq, batch_target in test_loader:
                output = model(batch_seq)
                _, predicted = torch.max(output.data, 1)
                total += batch_target.size(0)
                correct += (predicted == batch_target).sum().item()
        
        accuracy = 100 * correct / total
        print(f"Epoch [{epoch+1}/{EPOCHS}], Loss: {total_loss/len(train_loader):.4f}, Accuracy: {accuracy:.2f}%")
        
    # Save model
    torch.save(model.state_dict(), 'erickson_lstm_model.pth')
    print("Model saved to erickson_lstm_model.pth")
    
    # Show Top Predictions for a sample
    sample_seq = sequences[0]
    sample_input = torch.tensor([sample_seq], dtype=torch.long)
    model.eval()
    with torch.no_grad():
        output = model(sample_input)
        probs = torch.softmax(output, dim=1)
        top_probs, top_indices = torch.topk(probs, 5)
        
    print("\n--- Sample Prediction Example ---")
    print(f"Input History: {[idx_to_pattern[idx] for idx in sample_seq]}")
    print("Predicted Next Patterns:")
    for i in range(5):
        print(f"  {i+1}. {idx_to_pattern[top_indices[0][i].item()]} ({top_probs[0][i].item()*100:.2f}%)")

if __name__ == "__main__":
    train_model()
