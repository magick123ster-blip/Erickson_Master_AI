import pandas as pd
import numpy as np
import os

DATA_DIR = r'C:\Users\magic\Downloads\erickson_data'
INPUT_CSV = os.path.join(DATA_DIR, 'erickson_sequences.csv')

def extract_act3_shock_validation():
    df = pd.read_csv(INPUT_CSV)
    
    conv_keywords = ['Conversations With']
    conv_mask = df['script_id'].apply(lambda x: any(k in x for k in conv_keywords))
    conv_df = df[conv_mask].copy()
    conv_df = conv_df.sort_values(by=['script_id', 'turn_no'])
    
    print("=== ACT 3 (67-100%): SHOCK & VALIDATION EXAMPLES ===")
    
    for name, group in conv_df.groupby('script_id'):
        n_turns = len(group)
        if n_turns < 3: continue
        
        group = group.copy()
        group['rel_pos'] = np.linspace(0, 1, n_turns)
        
        # Get Act 3 rows
        act3 = group[group['rel_pos'] >= 0.66].copy()
        
        # Target specific patterns
        target_patterns = [
            'ERICKSON_SHOCK_PROVOCATION',
            'ERICKSON_CHALLENGE_PROVOCATION',
            'ERICKSON_PARADOXICAL_INTENTION',
            'ERICKSON_UTILIZATION_OF_RESISTANCE',
            'ERICKSON_PACING_AND_VALIDATION',
            'ERICKSON_YES_SET_PACING'
        ]
        
        targets = act3[act3['pattern_id'].isin(target_patterns)]
        
        if not targets.empty:
            for idx in targets.index:
                print(f"Script: {name}")
                print(f"Turn {act3.loc[idx, 'turn_no']}: [{act3.loc[idx, 'pattern_id']}]")
                print(f"Content: {act3.loc[idx, 'content']}")
                
                # Check next turn if exists in group
                next_turns = group[group['turn_no'] > act3.loc[idx, 'turn_no']]
                if not next_turns.empty:
                    next_row = next_turns.iloc[0]
                    print(f"--> NEXT [{next_row['pattern_id']}]: {next_row['content']}")
                print("-" * 50)

if __name__ == '__main__':
    extract_act3_shock_validation()
