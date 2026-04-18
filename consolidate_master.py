import json
import pandas as pd
import spacy
from tqdm import tqdm

# Load spaCy
nlp = spacy.load("en_core_web_sm")

def load_base_data(file_path):
    print(f"Loading base data from {file_path}...")
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data.append(json.loads(line))
            except:
                continue
    return data

def consolidate_master(jsonl_src, output_csv):
    base_data = load_base_data(jsonl_src)
    master_list = []
    
    # Load separate analysis results if available
    try:
        topic_df = pd.read_csv('erickson_topic_analysis_raw.csv')
    except:
        topic_df = None
        
    try:
        results_df = pd.read_csv('analysis_results.csv') # contains cluster from schema_extraction.py
    except:
        results_df = None

    print(f"Consolidating {len(base_data)} entries...")
    for i, item in enumerate(tqdm(base_data)):
        txt = item.get('output', '')
        doc = nlp(txt)
        
        # 1. Basic NLP
        is_passive = any(t.dep_ == "auxpass" for t in doc)
        suggestive_verbs = ["wonder", "discover", "notice", "allow", "permit", "find", "begin", "realize", "learn", "feel"]
        found_verbs = [t.lemma_.lower() for t in doc if t.lemma_.lower() in suggestive_verbs and t.pos_ == "VERB"]
        
        # 2. SVO (Simplified)
        svos = []
        for token in doc:
            if token.pos_ == "VERB":
                subj = [w.text.lower() for w in token.lefts if "subj" in w.dep_]
                obj = [w.text.lower() for w in token.rights if w.dep_ in ["dobj", "pobj", "attr"]]
                if subj and obj:
                    svos.append(f"{subj[0]}->{token.lemma_.lower()}->{obj[0]}")

        entry = {
            'index': i,
            'pattern_id': item.get('pattern_id', 'UNKNOWN'),
            'output': txt,
            'is_passive': is_passive,
            'suggestive_verbs': ", ".join(set(found_verbs)),
            'svo_structure': "; ".join(svos[:2]), # Top 2
            'cognitive_frame': results_df.iloc[i]['cluster'] if results_df is not None and i < len(results_df) else "N/A",
            'dominant_topic': topic_df.iloc[i]['dominant_topic'] if topic_df is not None and i < len(topic_df) else "N/A",
            'context': str(item.get('context_analysis', '')),
            'reasoning': str(item.get('reasoning_trace', ''))
        }
        master_list.append(entry)

    df = pd.DataFrame(master_list)
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"Master data saved to {output_csv}")

if __name__ == "__main__":
    src = r'C:\Users\magic\Downloads\erickson_data\augmented_scripts_full.jsonl'
    out = 'erickson_master_analysis_data.csv'
    consolidate_master(src, out)
