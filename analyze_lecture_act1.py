import pandas as pd
import numpy as np
import os

DATA_DIR = r'C:\Users\magic\Downloads\erickson_data'
INPUT_CSV = os.path.join(DATA_DIR, 'erickson_sequences.csv')

def analyze_lecture_act1():
    df = pd.read_csv(INPUT_CSV)
    
    lecture_keywords = ['Seminar', 'Teaching', 'Lecture', 'Workshop']
    lecture_mask = df['script_id'].apply(lambda x: any(k in x for k in lecture_keywords))
    lecture_df = df[lecture_mask].copy()
    lecture_df = lecture_df.sort_values(by=['script_id', 'turn_no'])
    
    act1_rows = []
    
    for name, group in lecture_df.groupby('script_id'):
        n_turns = len(group)
        if n_turns < 3: continue
        group = group.copy()
        group['rel_pos'] = np.linspace(0, 1, n_turns)
        act1 = group[group['rel_pos'] < 0.33].copy()
        act1_rows.append(act1)
        
    act1_df = pd.concat(act1_rows)
    
    print("\n=== LECTURE ACT 1: Most Frequently Used Micro Patterns ===")
    print(act1_df['pattern_id'].value_counts().head(10))
    
    transitions = []
    for name, group in act1_df.groupby('script_id'):
        patterns = group['pattern_id'].tolist()
        for i in range(len(patterns) - 1):
            transitions.append(f"{patterns[i]} -> {patterns[i+1]}")
            
    print("\n=== LECTURE ACT 1: Most Frequent Sequential Chains (Pairs) ===")
    print(pd.Series(transitions).value_counts().head(10))
    
    triplets = []
    for name, group in act1_df.groupby('script_id'):
        patterns = group['pattern_id'].tolist()
        for i in range(len(patterns) - 2):
            triplets.append(f"{patterns[i]} -> {patterns[i+1]} -> {patterns[i+2]}")
            
    print("\n=== LECTURE ACT 1: Most Frequent 3-Step Sequential Chains ===")
    print(pd.Series(triplets).value_counts().head(5))

if __name__ == '__main__':
    analyze_lecture_act1()
