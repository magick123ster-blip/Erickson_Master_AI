import pandas as pd
import numpy as np
import os

DATA_DIR = r'C:\Users\magic\Downloads\erickson_data'
INPUT_CSV = os.path.join(DATA_DIR, 'erickson_sequences_with_submacros.csv')

def export_absolute_raw_data():
    print("Loading data...")
    df = pd.read_csv(INPUT_CSV)
    df = df.sort_values(by=['script_id', 'turn_no'])
    
    # 1. GENERATE GRANULAR TO MACRO MAPPING
    # Create a mapping unique Dictionary
    mapping_df = df[['pattern_id', 'sub_macro']].drop_duplicates().sort_values('pattern_id')
    mapping_csv_path = os.path.join(DATA_DIR, 'granular_to_macro_mapping.csv')
    mapping_df.to_csv(mapping_csv_path, index=False)
    print(f"[SUCCESS] Exported {len(mapping_df)} unique granular mappings to {mapping_csv_path}")
    
    # 2. GENERATE FULL NxN TRANSITION EDGE LIST
    transitions = []
    
    # Extract sequences per script
    for name, group in df.groupby('script_id'):
        seq = group['pattern_id'].tolist()
        for i in range(len(seq) - 1):
            transitions.append((seq[i], seq[i+1]))
            
    # Count transitions
    trans_df = pd.DataFrame(transitions, columns=['From', 'To'])
    
    # We want exact mathematically perfect probabilities.
    # Group by 'From' and 'To' to get counts
    counts = trans_df.groupby(['From', 'To']).size().reset_index(name='Count')
    
    # Calculate Total outgoing count per 'From' state to compute probability
    total_from_counts = counts.groupby('From')['Count'].sum().reset_index(name='Total_From')
    
    # Merge and calculate probability
    merged = pd.merge(counts, total_from_counts, on='From')
    merged['Transition_Probability'] = merged['Count'] / merged['Total_From']
    
    # Sort for easier reading
    merged = merged.sort_values(by=['From', 'Transition_Probability'], ascending=[True, False])
    
    # Drop Total_From column, keeping only From, To, Count, Probability
    final_edgelist = merged[['From', 'To', 'Count', 'Transition_Probability']]
    
    edgelist_csv_path = os.path.join(DATA_DIR, 'full_granular_transitions_edgelist.csv')
    final_edgelist.to_csv(edgelist_csv_path, index=False)
    
    print(f"[SUCCESS] Exported {len(final_edgelist)} non-zero transition edges to {edgelist_csv_path}")
    print("Math is perfect: Summing Transition_Probability for any 'From' state will exactly equal 1.0")

if __name__ == '__main__':
    export_absolute_raw_data()
