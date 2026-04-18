import pandas as pd
import numpy as np
import os

DATA_DIR = r'C:\Users\magic\Downloads\erickson_data'
INPUT_CSV = os.path.join(DATA_DIR, 'erickson_sequences.csv')

def analyze_conversation_structure():
    df = pd.read_csv(INPUT_CSV)
    df['macro'] = df['pattern_label'].str.upper().replace('DOUBLE BIND', 'DOUBLE_BIND')
    
    # Filter only Conversations scripts
    conv_keywords = ['Conversations With']
    conv_mask = df['script_id'].apply(lambda x: any(k in x for k in conv_keywords))
    
    conv_df = df[conv_mask].copy()
    conv_df = conv_df.sort_values(by=['script_id', 'turn_no'])
    
    print(f"Total Conversation Turns: {len(conv_df)}")
    
    phase_data = []
    
    for name, group in conv_df.groupby('script_id'):
        n_turns = len(group)
        if n_turns < 3: continue
        
        group = group.copy()
        group['rel_pos'] = np.linspace(0, 1, n_turns)
        
        conditions = [
            (group['rel_pos'] < 0.33),
            (group['rel_pos'] >= 0.33) & (group['rel_pos'] < 0.66),
            (group['rel_pos'] >= 0.66)
        ]
        choices = ['1_Beginning', '2_Middle', '3_Ending']
        group['Phase'] = np.select(conditions, choices, default='Unknown')
        
        phase_data.append(group)
        
    full_df = pd.concat(phase_data)
    
    # Macro Pattern Distribution by Phase
    crosstab_macro = pd.crosstab(full_df['Phase'], full_df['macro'], normalize='index') * 100
    print("\n=== CONVERSATION ARC: Macro Pattern Distribution by Phase (%) ===")
    print(crosstab_macro.round(2))
    
    # Micro Patterns for ACT 1, 2, 3
    for phase_name, title in [('1_Beginning', 'ACT 1: Early Conversation (0-33%)'), 
                              ('2_Middle', 'ACT 2: Middle Conversation (34-66%)'), 
                              ('3_Ending', 'ACT 3: Late Conversation (67-100%)')]:
        print(f"\n===============================")
        print(f"=== {title} ===")
        print("===============================\n")
        
        phase_df = full_df[full_df['Phase'] == phase_name]
        
        print("[Most Frequently Used Micro Patterns]")
        print(phase_df['pattern_id'].value_counts().head(5))
        
        transitions = []
        triplets = []
        # Group by script ID so we don't bleed edges
        for name, group in phase_df.groupby('script_id'):
            patterns = group['pattern_id'].tolist()
            for i in range(len(patterns) - 1):
                transitions.append(f"{patterns[i]} -> {patterns[i+1]}")
            for i in range(len(patterns) - 2):
                triplets.append(f"{patterns[i]} -> {patterns[i+1]} -> {patterns[i+2]}")
                
        print("\n[Most Frequent 2-Step Chains]")
        print(pd.Series(transitions).value_counts().head(5))
        
        print("\n[Most Frequent 3-Step Chains]")
        print(pd.Series(triplets).value_counts().head(3))

if __name__ == '__main__':
    analyze_conversation_structure()
