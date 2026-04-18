import pandas as pd
import numpy as np
import os

DATA_DIR = r'C:\Users\magic\Downloads\erickson_data'
INPUT_CSV = os.path.join(DATA_DIR, 'erickson_sequences_with_submacros.csv')

def analyze_unified_markov():
    print("Loading data for Unified Markov Analysis...")
    df = pd.read_csv(INPUT_CSV)
    df = df.sort_values(by=['script_id', 'turn_no'])
    
    transitions = []
    
    for name, group in df.groupby('script_id'):
        seq = group['sub_macro'].tolist()
        for i in range(len(seq) - 1):
            transitions.append((seq[i], seq[i+1]))
            
    trans_df = pd.DataFrame(transitions, columns=['From', 'To'])
    
    crosstab = pd.crosstab(trans_df['From'], trans_df['To'], normalize='index') * 100
    
    print("\n=== UNIFIED 13-STATE MARKOV TRANSITION MATRIX (%) ===")
    print(crosstab.round(1))
    
    # Save the full matrix to CSV for reference
    crosstab.round(2).to_csv(os.path.join(DATA_DIR, 'unified_13_state_markov.csv'))
    
    print("\n=== TOP GLOBAL TRANSITIONS (Strongest Chains) ===")
    # Extract the highest probability transitions (excluding self-transitions unless they are very high)
    top_transitions = []
    for from_state in crosstab.index:
        for to_state in crosstab.columns:
            prob = crosstab.loc[from_state, to_state]
            if prob > 15.0:  # Arbitrary threshold to find the very strongest links
                top_transitions.append((from_state, to_state, prob))
                
    top_transitions.sort(key=lambda x: x[2], reverse=True)
    for f, t, p in top_transitions:
        print(f"{f}  ==>  {t}  ({p:.1f}%)")

if __name__ == '__main__':
    analyze_unified_markov()
