import json
import spacy
from collections import Counter
import pandas as pd

# Load spaCy
nlp = spacy.load("en_core_web_sm")

def extract_svo_and_modifiers(texts, limit=1000):
    print(f"Extracting syntactic structures from {limit} sentences...")
    svo_patterns = Counter()
    modifier_patterns = Counter() # verb -> modifier
    
    for doc in nlp.pipe(texts[:limit], batch_size=50):
        for token in doc:
            # 1. SVO Extraction (simplified)
            if token.pos_ == "VERB":
                subj = [w.text.lower() for w in token.lefts if w.dep_ in ["nsubj", "nsubjpass"]]
                obj = [w.text.lower() for w in token.rights if w.dep_ in ["dobj", "pobj", "attr"]]
                
                if subj and obj:
                    for s in subj:
                        for o in obj:
                            svo_patterns[f"{s} -> {token.lemma_.lower()} -> {o}"] += 1
                
                # 2. Modifiers for Verbs (Advmod)
                advmods = [w.text.lower() for w in token.children if w.dep_ == "advmod"]
                for adv in advmods:
                    modifier_patterns[f"{adv} {token.lemma_.lower()}"] += 1

    return svo_patterns, modifier_patterns

if __name__ == "__main__":
    file_path = r'C:\Users\magic\Downloads\erickson_data\augmented_scripts_full.jsonl'
    with open(file_path, 'r', encoding='utf-8') as f:
        texts = [json.loads(line).get('output', '') for line in f]
    
    svo, mods = extract_svo_and_modifiers(texts, limit=2000)
    
    print("\n## Syntactic Analysis (Sample Size: 2000)")
    
    print("\n### Top 10 SVO / Core Structures")
    for pattern, count in svo.most_common(10):
        print(f"- {pattern}: {count}")
        
    print("\n### Top 10 Verb Modifiers (Advmod)")
    for pattern, count in mods.most_common(10):
        print(f"- {pattern}: {count}")

    # Save summary for report
    summary = {
        "svo": dict(svo.most_common(50)),
        "modifiers": dict(mods.most_common(50))
    }
    with open('syntax_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
