import pandas as pd
import numpy as np
import os

DATA_DIR = r'C:\Users\magic\Downloads\erickson_data'
INPUT_CSV = os.path.join(DATA_DIR, 'erickson_sequences.csv')

def analyze_lecture_structure():
    df = pd.read_csv(INPUT_CSV)
    df['macro'] = df['pattern_label'].str.upper().replace('DOUBLE BIND', 'DOUBLE_BIND')
    
    # Filter only Lecture / Seminar / Workshop scripts
    lecture_keywords = ['Seminar', 'Teaching', 'Lecture', 'Workshop']
    lecture_mask = df['script_id'].apply(lambda x: any(k in x for k in lecture_keywords))
    
    lecture_df = df[lecture_mask].copy()
    lecture_df = lecture_df.sort_values(by=['script_id', 'turn_no'])
    
    print(f"Total Lecture/Seminar Turns: {len(lecture_df)}")
    
    phase_data = []
    
    for name, group in lecture_df.groupby('script_id'):
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
    
    # Macro Pattern Distribution by Phase in Lectures
    crosstab_macro = pd.crosstab(full_df['Phase'], full_df['macro'], normalize='index') * 100
    print("\n=== LECTURE ARC: Macro Pattern Distribution by Phase (%) ===")
    print(crosstab_macro.round(2))
    
    # Top 5 Micro patterns by Phase in Lectures
    print("\n=== LECTURE ARC: Top Micro Patterns ===")
    for phase in ['1_Beginning', '2_Middle', '3_Ending']:
        print(f"\n[{phase}]")
        print(full_df[full_df['Phase'] == phase]['pattern_id'].value_counts().head(5))

if __name__ == '__main__':
    analyze_lecture_structure()
