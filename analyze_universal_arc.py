import pandas as pd
import numpy as np
import os

DATA_DIR = r'C:\Users\magic\Downloads\erickson_data'
INPUT_CSV = os.path.join(DATA_DIR, 'erickson_sequences.csv')

def analyze_universal_arc():
    print("Loading sequence data to extract the universal arc...")
    df = pd.read_csv(INPUT_CSV)
    df['macro'] = df['pattern_label'].str.upper().replace('DOUBLE BIND', 'DOUBLE_BIND')
    df = df.sort_values(by=['script_id', 'turn_no'])
    
    # We will divide each session into 3 phases: Beginning (first 33%), Middle (middle 34%), End (last 33%)
    phase_data = []
    
    for name, group in df.groupby('script_id'):
        n_turns = len(group)
        if n_turns < 3: continue
        
        # Calculate relative position (0.0 to 1.0)
        group = group.copy()
        group['rel_pos'] = np.linspace(0, 1, n_turns)
        
        # Assign phases
        conditions = [
            (group['rel_pos'] < 0.33),
            (group['rel_pos'] >= 0.33) & (group['rel_pos'] < 0.66),
            (group['rel_pos'] >= 0.66)
        ]
        choices = ['1_Beginning', '2_Middle', '3_Ending']
        group['Phase'] = np.select(conditions, choices, default='Unknown')
        
        phase_data.append(group)
        
    full_df = pd.concat(phase_data)
    
    # Calculate distribution of macro patterns in each phase
    crosstab = pd.crosstab(full_df['Phase'], full_df['macro'], normalize='index') * 100
    print("\n=== Universal Arc: Macro Pattern Distribution by Phase (%) ===")
    print(crosstab.round(2))
    
    # Save the crosstab for the AI to read
    crosstab.to_csv(os.path.join(DATA_DIR, 'universal_arc_distribution.csv'))
    
if __name__ == '__main__':
    analyze_universal_arc()
