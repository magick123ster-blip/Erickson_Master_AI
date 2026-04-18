import pandas as pd
import numpy as np
import os

DATA_DIR = r'C:\Users\magic\Downloads\erickson_data'
INPUT_CSV = os.path.join(DATA_DIR, 'erickson_sequences.csv')

def analyze_lecture_act2_3():
    df = pd.read_csv(INPUT_CSV)
    
    lecture_keywords = ['Seminar', 'Teaching', 'Lecture', 'Workshop']
    lecture_mask = df['script_id'].apply(lambda x: any(k in x for k in lecture_keywords))
    lecture_df = df[lecture_mask].copy()
    lecture_df = lecture_df.sort_values(by=['script_id', 'turn_no'])
    
    act2_rows = []
    act3_rows = []
    
    for name, group in lecture_df.groupby('script_id'):
        n_turns = len(group)
        if n_turns < 3: continue
        group = group.copy()
        group['rel_pos'] = np.linspace(0, 1, n_turns)
        
        act2 = group[(group['rel_pos'] >= 0.33) & (group['rel_pos'] < 0.66)].copy()
        act3 = group[group['rel_pos'] >= 0.66].copy()
        
        act2_rows.append(act2)
        act3_rows.append(act3)
        
    act2_df = pd.concat(act2_rows)
    act3_df = pd.concat(act3_rows)
    
    print("\n===============================")
    print("=== LECTURE ACT 2 (34% ~ 66%) ===")
    print("===============================")
    print("\n[ACT 2: Most Frequently Used Micro Patterns]")
    print(act2_df['pattern_id'].value_counts().head(10))
    
    act2_transitions = []
    for name, group in act2_df.groupby('script_id'):
        patterns = group['pattern_id'].tolist()
        for i in range(len(patterns) - 1):
            act2_transitions.append(f"{patterns[i]} -> {patterns[i+1]}")
    print("\n[ACT 2: Most Frequent 2-Step Chains]")
    print(pd.Series(act2_transitions).value_counts().head(5))
    
    act2_triplets = []
    for name, group in act2_df.groupby('script_id'):
        patterns = group['pattern_id'].tolist()
        for i in range(len(patterns) - 2):
            act2_triplets.append(f"{patterns[i]} -> {patterns[i+1]} -> {patterns[i+2]}")
    print("\n[ACT 2: Most Frequent 3-Step Chains]")
    print(pd.Series(act2_triplets).value_counts().head(3))
    
    print("\n===============================")
    print("=== LECTURE ACT 3 (67% ~ 100%) ===")
    print("===============================")
    print("\n[ACT 3: Most Frequently Used Micro Patterns]")
    print(act3_df['pattern_id'].value_counts().head(10))
    
    act3_transitions = []
    for name, group in act3_df.groupby('script_id'):
        patterns = group['pattern_id'].tolist()
        for i in range(len(patterns) - 1):
            act3_transitions.append(f"{patterns[i]} -> {patterns[i+1]}")
    print("\n[ACT 3: Most Frequent 2-Step Chains]")
    print(pd.Series(act3_transitions).value_counts().head(5))

    act3_triplets = []
    for name, group in act3_df.groupby('script_id'):
        patterns = group['pattern_id'].tolist()
        for i in range(len(patterns) - 2):
            act3_triplets.append(f"{patterns[i]} -> {patterns[i+1]} -> {patterns[i+2]}")
    print("\n[ACT 3: Most Frequent 3-Step Chains]")
    print(pd.Series(act3_triplets).value_counts().head(3))

if __name__ == '__main__':
    analyze_lecture_act2_3()
