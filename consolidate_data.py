import json
import pandas as pd
import spacy
from collections import Counter

# Load spaCy
nlp = spacy.load("en_core_web_sm")

# HMM States Map
HMM_STATES = {
    "RAPPORT": "Rapport Building",
    "RESISTANCE": "Resistance Bypassing",
    "METAPHOR": "Metaphor Insertion",
    "ACTION": "Call to Action"
}

STATE_MAPPING = {
    "ERICKSON_TRUISM_PACING": "RAPPORT", "ERICKSON_PACING_AND_RAPPORT": "RAPPORT", "ERICKSON_TRUISM": "RAPPORT",
    "ERICKSON_SHOCK_TRUISM": "RESISTANCE", "ERICKSON_PATTERN_INTERRUPT": "RESISTANCE",
    "ERICKSON_METAPHOR": "METAPHOR", "ERICKSON_ANECDOTE_DIRECTIVE": "METAPHOR",
    "ERICKSON_ORDEAL_THERAPY": "ACTION", "ERICKSON_DIRECT_SUGGESTION": "ACTION"
}

def get_hmm_state(pattern_id):
    if pattern_id in STATE_MAPPING: return STATE_MAPPING[pattern_id]
    p = pattern_id.lower()
    if any(k in p for k in ["rapport", "pacing", "truism"]): return "RAPPORT"
    if any(k in p for k in ["shock", "confusion", "interrupt"]): return "RESISTANCE"
    if any(k in p for k in ["metaphor", "anecdote", "analogy"]): return "METAPHOR"
    if any(k in p for k in ["suggestion", "directive", "action"]): return "ACTION"
    return "RAPPORT"

def generate_raw_data(file_path, output_csv, limit=2000):
    print(f"Generating raw data for {limit} entries...")
    data = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        count = 0
        for line in f:
            if count >= limit: break
            try:
                item = json.loads(line)
                txt = item.get('output', '')
                pid = item.get('pattern_id', 'UNKNOWN')
                
                # NLP Analysis
                doc = nlp(txt)
                is_passive = any(t.dep_ == "auxpass" for t in doc)
                suggestive_verbs = ["wonder", "discover", "notice", "allow", "permit", "find", "begin", "realize", "learn", "feel"]
                found_verbs = [t.lemma_.lower() for t in doc if t.lemma_.lower() in suggestive_verbs and t.pos_ == "VERB"]
                
                data.append({
                    'pattern_id': pid,
                    'hmm_state': HMM_STATES.get(get_hmm_state(pid), 'Rapport Building'),
                    'is_passive': is_passive,
                    'suggestive_verbs': ", ".join(set(found_verbs)),
                    'context': str(item.get('context_analysis', '')),
                    'reasoning': str(item.get('reasoning_trace', '')),
                    'output': txt
                })
                count += 1
            except:
                continue

    df = pd.DataFrame(data)
    # Add cluster if exists from previous analysis
    try:
        results_df = pd.read_csv('analysis_results.csv')
        df['cognitive_frame_id'] = results_df['cluster'].head(limit)
    except:
        pass
        
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"Raw data saved to {output_csv}")

if __name__ == "__main__":
    src = r'C:\Users\magic\Downloads\erickson_data\augmented_scripts_full.jsonl'
    out = 'erickson_raw_analysis_data.csv'
    generate_raw_data(src, out)
