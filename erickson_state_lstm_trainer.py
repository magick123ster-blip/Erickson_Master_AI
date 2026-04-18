import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import numpy as np
import collections
import json
from sklearn.model_selection import train_test_split

# 1. Configuration
WINDOW_SIZE = 5
EMBEDDING_DIM = 32
HIDDEN_DIM = 64
BATCH_SIZE = 32
EPOCHS = 30
LEARNING_RATE = 0.001

# 2. State Mapping Logic (Same as HMM Analysis)
STATE_MAP = {
    'UTILIZATION': 'STATE_UTIL', 'RESOURCE': 'STATE_UTIL', 'ACCEPTANCE': 'STATE_UTIL', 'ALLIANCE': 'STATE_UTIL',
    'TRUISM': 'STATE_PACE', 'PACING': 'STATE_PACE', 'VALIDATION': 'STATE_PACE', 'YES': 'STATE_PACE', 
    'SET': 'STATE_PACE', 'RATIFICATION': 'STATE_PACE', 'MATCHING': 'STATE_PACE', 'REINFORCEMENT': 'STATE_PACE',
    'SUGGESTION': 'STATE_SUGG', 'DIRECT': 'STATE_SUGG', 'INDIRECT': 'STATE_SUGG', 'COMMAND': 'STATE_SUGG', 
    'REFRAMING': 'STATE_REFRAME', 'PARADOX': 'STATE_REFRAME', 'REDEFINITION': 'STATE_REFRAME', 'REFRAME': 'STATE_REFRAME',
    'PRESUPPOSITION': 'STATE_BIND', 'BIND': 'STATE_BIND', 'DOUBLE': 'STATE_BIND', 'CHOICE': 'STATE_BIND', 
    'DISSOCIATION': 'STATE_DISSOC', 'UNCONSCIOUS': 'STATE_DISSOC', 'AMNESIA': 'STATE_DISSOC', 'TRANCE': 'STATE_DISSOC', 
    'INQUIRY': 'STATE_INQUIRY', 'QUESTION': 'STATE_INQUIRY', 'PROBE': 'STATE_INQUIRY',
    'METAPHOR': 'STATE_METAPHOR', 'ANECDOTE': 'STATE_METAPHOR', 'STORY': 'STATE_METAPHOR', 'ANALOGY': 'STATE_METAPHOR',
    'RESISTANCE': 'STATE_INTERRUPT', 'INTERRUPT': 'STATE_INTERRUPT', 'INTERRUPTION': 'STATE_INTERRUPT', 'SHOCK': 'STATE_INTERRUPT', 
    'CHALLENGE': 'STATE_INTERRUPT', 'CONFUSION': 'STATE_INTERRUPT', 'STRATEGIC': 'STATE_INTERRUPT'
}

def get_state(pid):
    if not isinstance(pid, str): return 'STATE_UNKNOWN'
    parts = pid.upper().split('_')
    counts = collections.Counter()
    for p in parts:
        if p in STATE_MAP: counts[STATE_MAP[p]] += 1
    return counts.most_common(1)[0][0] if counts else 'STATE_UNKNOWN'

class StateDataset(Dataset):
    def __init__(self, sequences, targets):
        self.sequences = torch.tensor(sequences, dtype=torch.long)
        self.targets = torch.tensor(targets, dtype=torch.long)
    def __len__(self): return len(self.targets)
    def __getitem__(self, idx): return self.sequences[idx], self.targets[idx]

class StateLSTM(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim):
        super(StateLSTM, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True, num_layers=2, dropout=0.2)
        self.fc = nn.Linear(hidden_dim, output_dim)
    def forward(self, x):
        embeds = self.embedding(x)
        lstm_out, _ = self.lstm(embeds)
        return self.fc(lstm_out[:, -1, :])

def train():
    df = pd.read_csv('erickson_sequences_with_submacros.csv')
    df['state'] = df['pattern_id'].apply(get_state)
    
    states = sorted(df['state'].unique().tolist())
    state_to_idx = {s: i for i, s in enumerate(states)}
    idx_to_state = {i: s for s, i in state_to_idx.items()}
    
    sequences, targets = [], []
    for script_id, group in df.groupby('script_id'):
        s_indices = [state_to_idx[s] for s in group.sort_values('turn_no')['state']]
        for i in range(WINDOW_SIZE, len(s_indices)):
            sequences.append(s_indices[i-WINDOW_SIZE:i])
            targets.append(s_indices[i])
            
    X_train, X_test, y_train, y_test = train_test_split(sequences, targets, test_size=0.15, random_state=42)
    
    train_loader = DataLoader(StateDataset(X_train, y_train), batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(StateDataset(X_test, y_test), batch_size=BATCH_SIZE)
    
    model = StateLSTM(len(states), EMBEDDING_DIM, HIDDEN_DIM, len(states))
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
    
    print(f"Training on 9 Data-Driven States (Total Sequences: {len(sequences)})")
    for epoch in range(EPOCHS):
        model.train()
        for b_seq, b_target in train_loader:
            optimizer.zero_grad(); loss = criterion(model(b_seq), b_target); loss.backward(); optimizer.step()
        
        model.eval(); correct, total = 0, 0
        with torch.no_grad():
            for b_seq, b_target in test_loader:
                _, pred = torch.max(model(b_seq), 1); total += b_target.size(0); correct += (pred == b_target).sum().item()
        
        if (epoch+1) % 5 == 0:
            print(f"Epoch [{epoch+1}/{EPOCHS}], Accuracy: {100 * correct / total:.2f}%")
            
    torch.save(model.state_dict(), 'erickson_state_lstm.pth')
    print("Model saved. Top Prediction for latest sequence:")
    
    sample_seq = sequences[-1]
    model.eval()
    with torch.no_grad():
        output = model(torch.tensor([sample_seq]))
        probs = torch.softmax(output, dim=1)
        top_p, top_i = torch.topk(probs, 3)
        print(f"History: {[idx_to_state[i] for i in sample_seq]}")
        for i in range(3):
            print(f"  -> {idx_to_state[top_i[0][i].item()]}: {top_p[0][i].item()*100:.2f}%")

if __name__ == "__main__":
    train()
