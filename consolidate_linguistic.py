import json
import spacy
import pandas as pd
from tqdm import tqdm

# Load spaCy
nlp = spacy.load("en_core_web_sm")

def generate_linguistic_csv(file_path, output_csv, limit=2000):
    print(f"Generating linguistic raw data for {limit} entries...")
    data = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()[:limit]
        
    for line in tqdm(lines):
        try:
            item = json.loads(line)
            txt = item.get('output', '')
            doc = nlp(txt)
            
            # 1. POS Sequence
            pos_seq = " ".join([t.pos_ for t in doc])
            
            # 2. SVO Extraction
            svos = []
            for token in doc:
                if token.pos_ == "VERB":
                    subj = [w.text.lower() for w in token.lefts if w.dep_ in ["nsubj", "nsubjpass"]]
                    obj = [w.text.lower() for w in token.rights if w.dep_ in ["dobj", "pobj", "attr"]]
                    if subj and obj:
                        for s in subj:
                            for o in obj:
                                svos.append(f"{s}->{token.lemma_.lower()}->{o}")
            
            # 3. Main Modifiers (Advmods)
            mods = [f"{t.text.lower()}_{t.head.lemma_.lower()}" for t in doc if t.dep_ == "advmod"]
            
            data.append({
                'text': txt,
                'pos_sequence': pos_seq,
                'svo_structures': "; ".join(svos),
                'verb_modifiers': "; ".join(mods),
                'pattern_id': item.get('pattern_id', 'UNKNOWN')
            })
        except:
            continue

    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"Linguistic raw data saved to {output_csv}")

if __name__ == "__main__":
    src = r'C:\Users\magic\Downloads\erickson_data\augmented_scripts_full.jsonl'
    out = 'erickson_linguistic_analysis_raw.csv'
    generate_linguistic_csv(src, out)
