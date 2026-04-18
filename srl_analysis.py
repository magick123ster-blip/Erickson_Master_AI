import json
import spacy
import pandas as pd
from tqdm import tqdm

# Load spaCy
nlp = spacy.load("en_core_web_sm")

def extract_semantic_roles(texts, limit=1000):
    print(f"Extracting Semantic Roles (SRL-like) from {limit} entries...")
    results = []
    
    for doc in tqdm(nlp.pipe(texts[:limit], batch_size=50), total=limit):
        roles = []
        for token in doc:
            if token.pos_ == "VERB":
                # Agent (Who)
                agents = [w.text.lower() for w in token.lefts if "subj" in w.dep_]
                # Patient/Theme (What)
                patients = [w.text.lower() for w in token.rights if w.dep_ in ["dobj", "pobj", "attr"]]
                # Manner (How)
                manners = [w.text.lower() for w in token.children if w.dep_ == "advmod"]
                # Location (Where)
                locations = [w.text.lower() for w in token.children if w.dep_ == "prep" and any(e.ent_type_ in ["GPE", "LOC", "FAC"] for e in w.subtree)]
                
                if agents or patients or manners:
                    roles.append({
                        "predicate": token.lemma_.lower(),
                        "agent": ", ".join(agents) if agents else "N/A",
                        "patient": ", ".join(patients) if patients else "N/A",
                        "manner": ", ".join(manners) if manners else "N/A",
                        "location": ", ".join(locations) if locations else "N/A"
                    })
        results.append(roles)
    return results

if __name__ == "__main__":
    file_path = r'C:\Users\magic\Downloads\erickson_data\augmented_scripts_full.jsonl'
    with open(file_path, 'r', encoding='utf-8') as f:
        texts = [json.loads(line).get('output', '') for line in f]
    
    sample_limit = 2000
    srl_results = extract_semantic_roles(texts, limit=sample_limit)
    
    # Flatten results for CSV
    flattened_data = []
    for i, res_list in enumerate(srl_results):
        for res in res_list:
            res['entry_id'] = i
            res['original_text'] = texts[i]
            flattened_data.append(res)
            
    df = pd.DataFrame(flattened_data)
    df.to_csv('erickson_srl_analysis_raw.csv', index=False, encoding='utf-8-sig')
    print(f"SRL-like analysis saved to erickson_srl_analysis_raw.csv")

    # Simple Summary
    print("\n## Top Predicates and their Roles")
    if not df.empty:
        print(df['predicate'].value_counts().head(10))
