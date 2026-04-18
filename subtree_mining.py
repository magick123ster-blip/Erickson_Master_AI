import json
import spacy
from collections import Counter
import pandas as pd
from tqdm import tqdm

# Load spaCy
nlp = spacy.load("en_core_web_sm")

def extract_subtrees(texts, limit=2000):
    print(f"Extracting Dependency Subtrees from {limit} entries...")
    subtree_counts = Counter()
    
    for doc in tqdm(nlp.pipe(texts[:limit], batch_size=50), total=limit):
        for token in doc:
            # We define a "subtree" as a node and its children (1-level deep structural template)
            # Pattern format: [Parent_POS]--[Dep_Rel]-->[Child_POS]
            
            children = list(token.children)
            if not children:
                continue
            
            # Create a localized structural signature
            # Example: VERB(nsubj:PRON, dobj:NOUN, advmod:ADV)
            child_sigs = sorted([f"{c.dep_}:{c.pos_}" for c in children])
            signature = f"{token.pos_}({', '.join(child_sigs)})"
            
            # Filter for meaningful signatures (usually centered around VERB or NOUN)
            if token.pos_ in ["VERB", "AUX", "NOUN"]:
                subtree_counts[signature] += 1
                
            # Also extract longer chains (Reasoning paths)
            # Pattern: Grandparent --dep--> Parent --dep--> Child
            for child in children:
                for grandchild in child.children:
                    chain = f"{token.pos_}--{child.dep_}-->{child.pos_}--{grandchild.dep_}-->{grandchild.pos_}"
                    subtree_counts[chain] += 1

    return subtree_counts

if __name__ == "__main__":
    file_path = r'C:\Users\magic\Downloads\erickson_data\augmented_scripts_full.jsonl'
    with open(file_path, 'r', encoding='utf-8') as f:
        texts = [json.loads(line).get('output', '') for line in f]
    
    sample_size = 3000 # Increased sample for FSM
    patterns = extract_subtrees(texts, limit=sample_size)
    
    print("\n## Frequent Subtree Patterns (Structural Templates)")
    top_patterns = patterns.most_common(50)
    for pat, count in top_patterns[:20]:
        print(f"- {pat}: {count}")
    
    # Save raw data for user
    data = [{"pattern": p, "count": c} for p, c in top_patterns]
    df = pd.DataFrame(data)
    df.to_csv('erickson_fsm_analysis_raw.csv', index=False, encoding='utf-8-sig')
    print("\nFSM analysis saved to erickson_fsm_analysis_raw.csv")
