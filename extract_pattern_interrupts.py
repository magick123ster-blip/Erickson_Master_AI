import pandas as pd
import numpy as np
import os

DATA_DIR = r'C:\Users\magic\Downloads\erickson_data'
INPUT_CSV = os.path.join(DATA_DIR, 'erickson_sequences.csv')

def extract_interrupts():
    df = pd.read_csv(INPUT_CSV)
    
    # Filter only Conversations scripts
    conv_keywords = ['Conversations With']
    conv_mask = df['script_id'].apply(lambda x: any(k in x for k in conv_keywords))
    conv_df = df[conv_mask].copy()
    conv_df = conv_df.sort_values(by=['script_id', 'turn_no'])
    
    print("=== PATTERN INTERRUPT EXAMPLES IN ACT 1 ===")
    
    for name, group in conv_df.groupby('script_id'):
        n_turns = len(group)
        if n_turns < 3: continue
        
        group = group.copy()
        group['rel_pos'] = np.linspace(0, 1, n_turns)
        
        # Get Act 1 rows
        act1 = group[group['rel_pos'] < 0.33].copy()
        
        # Find pattern interruptions
        interrupts = act1[act1['pattern_id'] == 'ERICKSON_PATTERN_INTERRUPTION']
        
        if not interrupts.empty:
            for idx in interrupts.index:
                # Get the turn and the one immediately following it (if available) to see the transition
                print(f"Script: {name}")
                print(f"Turn {act1.loc[idx, 'turn_no']}: [{act1.loc[idx, 'pattern_id']}]")
                print(f"Content: {act1.loc[idx, 'content']}")
                
                # Check next turn if exists in group
                next_turns = group[group['turn_no'] > act1.loc[idx, 'turn_no']]
                if not next_turns.empty:
                    next_row = next_turns.iloc[0]
                    print(f"--> NEXT [{next_row['pattern_id']}]: {next_row['content']}")
                print("-" * 50)

if __name__ == '__main__':
    extract_interrupts()
