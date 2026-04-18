import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import numpy as np
import collections
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 1. Configuration
WINDOW_SIZE = 5
STATE_EMBED_DIM = 16
NUM_FEATURES = 4 # passive, cog_frame, dom_topic, length
HIDDEN_DIM = 64
BATCH_SIZE = 32
EPOCHS = 30

# 2. State Mapping (Same as before)
STATE_MAP = {
    'UTILIZATION': 'STATE_UTIL', 'RESOURCE': 'STATE_UTIL', 'ACCEPTANCE': 'STATE_UTIL',
    'TRUISM': 'STATE_PACE', 'PACING': 'STATE_PACE', 'VALIDATION': 'STATE_PACE', 
    'SUGGESTION': 'STATE_SUGG', 'DIRECT': 'STATE_SUGG', 'INDIRECT': 'STATE_SUGG',
    'REFRAMING': 'STATE_REFRAME', 'PARADOX': 'STATE_REFRAME', 'REDEFINITION': 'STATE_REFRAME',
    'PRESUPPOSITION': 'STATE_BIND', 'BIND': 'STATE_BIND', 'DOUBLE': 'STATE_BIND',
    'DISSOCIATION': 'STATE_DISSOC', 'UNCONSCIOUS': 'STATE_DISSOC', 'AMNESIA': 'STATE_DISSOC',
    'INQUIRY': 'STATE_INQUIRY', 'QUESTION': 'STATE_INQUIRY',
    'METAPHOR': 'STATE_METAPHOR', 'ANECDOTE': 'STATE_METAPHOR',
    'RESISTANCE': 'STATE_INTERRUPT', 'INTERRUPT': 'STATE_INTERRUPT', 'SHOCK': 'STATE_INTERRUPT'
}

def get_state(pid):
    if not isinstance(pid, str): return 'STATE_UNKNOWN'
    parts = pid.upper().split('_')
    counts = collections.Counter()
    for p in parts:
        if p in STATE_MAP: counts[STATE_MAP[p]] += 1
    return counts.most_common(1)[0][0] if counts else 'STATE_UNKNOWN'

class HybridDataset(Dataset):
    def __init__(self, state_seqs, feature_seqs, targets):
        self.state_seqs = torch.tensor(state_seqs, dtype=torch.long)
        self.feature_seqs = torch.tensor(feature_seqs, dtype=torch.float32)
        self.targets = torch.tensor(targets, dtype=torch.long)
    def __len__(self): return len(self.targets)
    def __getitem__(self, idx): return self.state_seqs[idx], self.feature_seqs[idx], self.targets[idx]

class HybridLSTM(nn.Module):
    def __init__(self, vocab_size, embed_dim, feature_dim, hidden_dim, output_dim):
        super(HybridLSTM, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        # Combine embedding and numerical features
        self.lstm = nn.LSTM(embed_dim + feature_dim, hidden_dim, batch_first=True, num_layers=2, dropout=0.2)
        self.fc = nn.Linear(hidden_dim, output_dim)
        
    def forward(self, state_x, feat_x):
        # state_x: [batch, seq_len], feat_x: [batch, seq_len, feature_dim]
        embeds = self.embedding(state_x)
        combined = torch.cat((embeds, feat_x), dim=2)
        lstm_out, _ = self.lstm(combined)
        return self.fc(lstm_out[:, -1, :])

def train():
    print("Loading and Merging Data...")
    df_seq = pd.read_csv('erickson_sequences_with_submacros.csv')
    df_master = pd.read_csv('erickson_master_analysis_data.csv')
    
    # Simple merge by alignment (order is known to be consistent)
    # We take features from master
    df_master['length'] = df_master['output'].str.len()
    df_master['passive_num'] = df_master['is_passive'].apply(lambda x: 1 if x == 'True' or x == True else 0)
    
    # We select features for the 6,628 rows in df_seq
    # Since df_seq is a subset of df_master (only turns with patterns)
    # and they are ordered, we use content matching to align features
    master_dict = {str(row['output']).strip().lower(): row for _, row in df_master.iterrows()}
    
    features_list = []
    valid_indices = []
    for idx, row in df_seq.iterrows():
        content = str(row['content']).strip().lower()
        if content in master_dict:
            m = master_dict[content]
            features_list.append([m['passive_num'], m['cognitive_frame'], m['dominant_topic'], m['length']])
            valid_indices.append(idx)
            
    df = df_seq.iloc[valid_indices].copy()
    feature_matrix = np.array(features_list)
    
    # Standardize features
    scaler = StandardScaler()
    feature_matrix = scaler.fit_transform(feature_matrix)
    
    df['state'] = df['pattern_id'].apply(get_state)
    states = sorted(df['state'].unique().tolist())
    state_to_idx = {s: i for i, s in enumerate(states)}
    
    state_seqs, feature_seqs, targets = [], [], []
    for script_id, group in df.groupby('script_id'):
        indices = group.index.tolist()
        if len(indices) < WINDOW_SIZE + 1: continue
        
        s_idx = [state_to_idx[df.loc[i, 'state']] for i in indices]
        f_idx = [feature_matrix[df.index.get_loc(i)] for i in indices]
        
        for i in range(WINDOW_SIZE, len(s_idx)):
            state_seqs.append(s_idx[i-WINDOW_SIZE:i])
            feature_seqs.append(f_idx[i-WINDOW_SIZE:i])
            targets.append(s_idx[i])
            
    X_s_train, X_s_test, X_f_train, X_f_test, y_train, y_test = train_test_split(
        state_seqs, feature_seqs, targets, test_size=0.15, random_state=42)
    
    train_loader = DataLoader(HybridDataset(X_s_train, X_f_train, y_train), batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(HybridDataset(X_s_test, X_f_test, y_test), batch_size=BATCH_SIZE)
    
    model = HybridLSTM(len(states), STATE_EMBED_DIM, NUM_FEATURES, HIDDEN_DIM, len(states))
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    print(f"Training Hybrid LSTM (States + Linguistic Features)...")
    for epoch in range(EPOCHS):
        model.train()
        for b_s, b_f, b_t in train_loader:
            optimizer.zero_grad(); loss = criterion(model(b_s, b_f), b_t); loss.backward(); optimizer.step()
            
        model.eval(); correct, total = 0, 0
        with torch.no_grad():
            for b_s, b_f, b_t in test_loader:
                _, pred = torch.max(model(b_s, b_f), 1); total += b_t.size(0); correct += (pred == b_t).sum().item()
        
        if (epoch+1) % 5 == 0:
            print(f"Epoch [{epoch+1}/{EPOCHS}], Accuracy: {100 * correct / total:.2f}%")

    print("\nHybrid Analysis Complete.")

if __name__ == "__main__":
    train()
