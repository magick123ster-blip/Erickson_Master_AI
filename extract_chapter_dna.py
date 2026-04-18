import pandas as pd
import json
import os

# Configuration
DATA_DIR = r'C:\Users\magic\Downloads\erickson_data'
INPUT_CSV = os.path.join(DATA_DIR, 'erickson_situational_best_10_bilingual.csv')
MASTER_CSV = os.path.join(DATA_DIR, 'erickson_master_analysis_data.csv')
OUTPUT_JSON = os.path.join(DATA_DIR, 'erickson_chapter_dna.json')

def extract_dna():
    df_best = pd.read_csv(INPUT_CSV)
    df_master = pd.read_csv(MASTER_CSV)
    steps = [f'step_{i}_id' for i in range(1, 10)]
    
    chapter_dna = {}
    
    for situation, group in df_best.groupby('situation'):
        all_pids = []
        pid_scores = {} # PID -> list of scores it appears in
        
        for row in group.itertuples():
            row_pids = []
            for col in steps:
                if hasattr(row, col) and not pd.isna(getattr(row, col)):
                    pid = getattr(row, col)
                    row_pids.append(pid)
                    if pid not in pid_scores: pid_scores[pid] = []
                    pid_scores[pid].append(row.score)
            all_pids.extend(row_pids)
        
        counts = pd.Series(all_pids).value_counts()
        total_steps = len(all_pids)
        top_7_pids = counts.head(7).index.tolist()
        
        dna_list = []
        for pid in top_7_pids:
            matches = df_master[df_master['pattern_id'] == pid]
            if not matches.empty:
                row = matches.iloc[0]
                
                # Probability: Local frequency / total steps in top 10 chains of this situation
                prob = float(counts[pid] / total_steps)
                # Importance: Max score of a chain this PID belongs to in this situation
                importance = float(max(pid_scores[pid])) if pid in pid_scores else 0.0
                
                dna_list.append({
                    "pattern_id": pid,
                    "formula": str(row.get('svo_structure', 'N/A')),
                    "logic": str(row.get('reasoning', 'N/A')),
                    "example": str(row.get('output', 'N/A')),
                    "importance": importance,
                    "probability": prob
                })
        
        chapter_dna[situation] = dna_list

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(chapter_dna, f, ensure_ascii=False, indent=4)
    
    print(f"Chapter DNA (Elite 7) extracted to: {OUTPUT_JSON}")

if __name__ == "__main__":
    extract_dna()
