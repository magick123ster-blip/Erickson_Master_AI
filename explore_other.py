import pandas as pd
import os

DATA_DIR = r'C:\Users\magic\Downloads\erickson_data'
INPUT_CSV = os.path.join(DATA_DIR, 'erickson_sequences.csv')

def explore_other():
    df = pd.read_csv(INPUT_CSV)
    df['macro'] = df['pattern_label'].str.upper().replace('DOUBLE BIND', 'DOUBLE_BIND')
    
    other_df = df[df['macro'] == 'OTHER']
    
    print("=== Total 'OTHER' occurrences ===")
    print(len(other_df))
    
    print("\n=== Top 20 Micro-patterns inside 'OTHER' ===")
    print(other_df['pattern_id'].value_counts().head(20))
    
    print("\n=== Unique Micro-patterns inside 'OTHER' ===")
    print(other_df['pattern_id'].nunique())

if __name__ == '__main__':
    explore_other()
