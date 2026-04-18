import pandas as pd
import json
import os

# Paths
DATA_DIR = r'C:\Users\magic\Downloads\erickson_data'
INPUT_70 = os.path.join(DATA_DIR, 'erickson_top_70_chains_for_translation.csv')
MASTER_DATA = os.path.join(DATA_DIR, 'erickson_master_analysis_data.csv')
OUTPUT_JSON = os.path.join(DATA_DIR, 'translation_input.json')

def extract_for_translation():
    df_70 = pd.read_csv(INPUT_70)
    patterns = set()
    for _, row in df_70.iterrows():
        patterns.update(row['chain_sequence'].split(' -> '))
    
    df_m = pd.read_csv(MASTER_DATA).drop_duplicates(subset='pattern_id')
    mapping = df_m[df_m['pattern_id'].isin(patterns)][['pattern_id', 'output']].set_index('pattern_id')['output'].to_dict()
    
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    
    print(f"Extraction successful: {len(mapping)} patterns saved to {OUTPUT_JSON}")

if __name__ == "__main__":
    extract_for_translation()
