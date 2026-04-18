import pandas as pd
import json
import os

# Configuration
DATA_DIR = r'C:\Users\magic\Downloads\erickson_data'
INPUT_70 = os.path.join(DATA_DIR, 'erickson_top_70_chains_for_translation.csv')
TRANS_JSON = os.path.join(DATA_DIR, 'translation_output.json')
OUTPUT_CSV = os.path.join(DATA_DIR, 'erickson_situational_best_10_bilingual.csv')

def merge_translations():
    df_70 = pd.read_csv(INPUT_70)
    with open(TRANS_JSON, 'r', encoding='utf-8') as f:
        trans_map = json.load(f)
    
    # Identify how many step columns exist
    step_id_cols = [c for c in df_70.columns if c.startswith('step_') and c.endswith('_id')]
    
    for id_col in step_id_cols:
        step_num = id_col.split('_')[1]
        ko_col = f"step_{step_num}_text_ko"
        
        # Apply translation map based on the ID column
        df_70[ko_col] = df_70[id_col].map(trans_map)
        
    df_70.to_csv(OUTPUT_CSV, index=False, encoding='utf-8-sig')
    print(f"Bilingual CSV created with {len(step_id_cols)} step columns: {OUTPUT_CSV}")

if __name__ == "__main__":
    merge_translations()
