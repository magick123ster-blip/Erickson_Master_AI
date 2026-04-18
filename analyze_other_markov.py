import pandas as pd
import numpy as np
import os

DATA_DIR = r'C:\Users\magic\Downloads\erickson_data'
INPUT_CSV = os.path.join(DATA_DIR, 'erickson_sequences.csv')

def categorize_other(pattern_id):
    pid = str(pattern_id).upper()
    if 'DISSOCIATION' in pid:
        return 'OTHER_DISSOCIATION'
    elif 'INQUIRY' in pid or 'QUESTION' in pid:
        return 'OTHER_INQUIRY'
    elif 'CHALLENGE' in pid or 'PROVOCATION' in pid or 'ORDEAL' in pid or 'SHOCK' in pid:
        return 'OTHER_CHALLENGE'
    elif 'MINIMAL' in pid or 'CUE' in pid or 'PROMPT' in pid or 'RATIFICATION' in pid or 'VALIDATION' in pid or 'ENCOURAGER' in pid:
        return 'OTHER_CUE_PROMPT'
    elif 'TIME' in pid or 'AMNESIA' in pid:
        return 'OTHER_TIME_AMNESIA'
    else:
        return 'OTHER_UNKNOWN'

def analyze_other_markov():
    df = pd.read_csv(INPUT_CSV)
    df['macro'] = df['pattern_label'].str.upper().replace('DOUBLE BIND', 'DOUBLE_BIND')
    
    # Apply Sub-Macro only to OTHER
    df['sub_macro'] = df.apply(lambda row: categorize_other(row['pattern_id']) if row['macro'] == 'OTHER' else row['macro'], axis=1)
    
    df = df.sort_values(by=['script_id', 'turn_no'])
    
    # 1. Build Transition Matrix entirely using ALL patterns (Macro + SubMacros)
    transitions = []
    
    for name, group in df.groupby('script_id'):
        seq = group['sub_macro'].tolist()
        for i in range(len(seq) - 1):
            if seq[i].startswith('OTHER_') or seq[i+1].startswith('OTHER_'):
                transitions.append((seq[i], seq[i+1]))
            
    trans_df = pd.DataFrame(transitions, columns=['From', 'To'])
    
    # Filter Crosstab to only show lines coming FROM an OTHER state to ANY state
    crosstab_from_other = pd.crosstab(trans_df['From'], trans_df['To'], normalize='index') * 100
    from_other_only = crosstab_from_other[crosstab_from_other.index.str.startswith('OTHER_')]
    
    print("=== State Transition FROM 'OTHER' Sub-Categories (%) ===")
    print(from_other_only.round(1))
    
    # Filter Crosstab to only show lines going TO an OTHER state from ANY state
    crosstab_to_other = pd.crosstab(trans_df['To'], trans_df['From'], normalize='index') * 100
    to_other_only = crosstab_to_other[crosstab_to_other.index.str.startswith('OTHER_')]
    
    print("\n=== State Transition TO 'OTHER' Sub-Categories (%) ===")
    print(to_other_only.round(1))

    # Also save full df with sub_macros for the Deep Learning step
    df.to_csv(os.path.join(DATA_DIR, 'erickson_sequences_with_submacros.csv'), index=False)
    print("\n[SUCCESS] Extracted Sub-Macros and saved to erickson_sequences_with_submacros.csv")

if __name__ == '__main__':
    analyze_other_markov()
