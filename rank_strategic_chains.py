import pandas as pd
import os

# Configuration
DATA_DIR = r'C:\Users\magic\Downloads\erickson_data'
ALL_CHAINS_FILE = os.path.join(DATA_DIR, 'erickson_all_strategic_chains.csv')
HIERARCHY_FILE = os.path.join(DATA_DIR, 'hierarchical_report_source.csv')
MASTER_FILE = os.path.join(DATA_DIR, 'erickson_master_analysis_data.csv')
OUTPUT_FINAL_TOP_70 = os.path.join(DATA_DIR, 'erickson_top_70_chains_for_translation.csv')

MAPPING = {
    "Rapport & Pacing": ["PACING", "RAPPORT", "MIRRORING", "YES", "ACCEPTANCE", "AFFIRMATION", "AGREEMENT", "ALLIANCE", "COMFORT"],
    "Resistance & Utilization": ["RESISTANCE", "UTILIZATION", "CHALLENGE", "CHALLENGING", "PARADOX", "SYMPTOM", "ORDEAL", "OPPONENT", "NEGATION"],
    "Confusion & Induction": ["AMBIGUITY", "CONFUSION", "FIXATION", "TRANCE", "INDUCTION", "IDEOMOTOR", "SHOCK", "INTERRUPT", "INTERRUPTION", "AMBIGUOUS"],
    "Deepening & Ratification": ["DEEP", "DEEPENING", "RATIFICATION", "VALIDATION", "REINFORCEMENT", "RATIFYING", "TIME", "INTENSE", "INTENSIFICATION"],
    "Metaphor & Narrative": ["METAPHOR", "STORYTELLING", "ANECDOTAL", "ANECDOTE", "ANALOGY", "SYMBOLIC", "TRANSFORMATIONAL", "NARRATIVE"],
    "Reframing & Insight": ["REFRAMING", "REFRAME", "TRANSFORMATION", "INSIGHT", "DISPLACEMENT", "REASSOCIATION", "REDEFINITION", "LOGIC", "COGNITIVE"],
    "Future Pacing & Integration": ["FUTURE", "PROGRESSION", "POSTHYPNOTIC", "INTEGRATION", "AMNESIA", "LEARNING", "GROWTH", "CAPACITY"]
}

def get_situation(category):
    cat_upper = str(category).upper()
    for sit, keywords in MAPPING.items():
        if any(kw in cat_upper for kw in keywords):
            return sit
    return "Others"

def rank_and_extract_for_translation():
    print("Loading data...")
    df_chains = pd.read_csv(ALL_CHAINS_FILE)
    df_h = pd.read_csv(HIERARCHY_FILE)
    df_m = pd.read_csv(MASTER_FILE)
    
    h_info = df_h.groupby('Pattern ID').agg({'Importance': 'max', 'Category': 'first'}).to_dict('index')
    df_m_unique = df_m.drop_duplicates(subset='pattern_id')
    master_lookup = df_m_unique.set_index('pattern_id')[['output', 'svo_structure']].to_dict('index')

    print("Ranking chains by Importance...")
    ranked_rows = []
    
    for _, row in df_chains.iterrows():
        sequence = row['chain_sequence'].split(' -> ')
        
        first_pid = sequence[0]
        first_info = h_info.get(first_pid, {'Category': 'UNKNOWN'})
        situation = get_situation(first_info['Category'])
        
        if situation == "Others":
            continue
            
        # Score = Average Importance of all nodes in the chain
        imp_scores = [h_info.get(pid, {'Importance': 0})['Importance'] for pid in sequence]
        score = sum(imp_scores) / len(imp_scores) if imp_scores else 0
        
        ranked_rows.append({
            "situation": situation,
            "score": score,
            "chain_sequence": row['chain_sequence'],
            "length": row['length']
        })

    df_ranked = pd.DataFrame(ranked_rows)
    
    top_70_list = []
    for sit in MAPPING.keys():
        sit_data = df_ranked[df_ranked['situation'] == sit].sort_values(by='score', ascending=False).head(10)
        top_70_list.append(sit_data)
    
    final_top_70 = pd.concat(top_70_list)
    
    # Enrichment
    final_rows = []
    for _, row in final_top_70.iterrows():
        seq = row['chain_sequence'].split(' -> ')
        new_row = {"situation": row['situation'], "score": row['score'], "chain_sequence": row['chain_sequence']}
        for i, pid in enumerate(seq):
            info = master_lookup.get(pid, {"output": "[N/A]", "svo_structure": "[N/A]"})
            new_row[f"step_{i+1}_id"] = pid
            new_row[f"step_{i+1}_text_en"] = info['output']
        final_rows.append(new_row)
        
    df_final = pd.DataFrame(final_rows)
    df_final.to_csv(OUTPUT_FINAL_TOP_70, index=False, encoding='utf-8-sig')
    print(f"Extraction complete. Top 70 chains saved to {OUTPUT_FINAL_TOP_70}")

if __name__ == "__main__":
    rank_and_extract_for_translation()
