import json
import pandas as pd
from mlxtend.frequent_patterns import fpgrowth, association_rules
from mlxtend.preprocessing import TransactionEncoder
from tqdm import tqdm

def load_data(file_path):
    print(f"Loading data from {file_path}...")
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data.append(json.loads(line))
            except:
                continue
    return data

import re
from collections import Counter

def get_top_words(data, top_n=100):
    print(f"Finding top {top_n} words across corpus...")
    all_words = []
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'was', 'were', 'to', 'for', 'in', 'of', 'on', 'at', 'with', 'by', 'this', 'that', 'with', 'from', 'it', 'they', 'you', 'me', 'him', 'her', 'them', 'have', 'your', 'about', 'when', 'there', 'what', 'which', 'their'}
    for item in data:
        text = str(item.get('context_analysis', '')) + " " + str(item.get('reasoning_trace', ''))
        words = re.findall(r'\w+', text.lower())
        all_words.extend([w for w in words if w not in stop_words and len(w) > 3])
    
    counts = Counter(all_words)
    return set([w for w, c in counts.most_common(top_n)])

# HMM States Map
HMM_STATE_MAP = {
    "ERICKSON_TRUISM_PACING": "RAPPORT", "ERICKSON_PACING_AND_RAPPORT": "RAPPORT", "ERICKSON_TRUISM": "RAPPORT",
    "ERICKSON_SHOCK_TRUISM": "RESISTANCE", "ERICKSON_PATTERN_INTERRUPT": "RESISTANCE",
    "ERICKSON_METAPHOR": "METAPHOR", "ERICKSON_ANECDOTE_DIRECTIVE": "METAPHOR",
    "ERICKSON_ORDEAL_THERAPY": "ACTION", "ERICKSON_DIRECT_SUGGESTION": "ACTION"
}

def get_hmm_state(pattern_id):
    if pattern_id in HMM_STATE_MAP: return HMM_STATE_MAP[pattern_id]
    p = str(pattern_id).lower()
    if any(k in p for k in ["rapport", "pacing", "truism"]): return "RAPPORT"
    if any(k in p for k in ["shock", "confusion", "interrupt"]): return "RESISTANCE"
    if any(k in p for k in ["metaphor", "anecdote", "analogy"]): return "METAPHOR"
    if any(k in p for k in ["suggestion", "directive", "action"]): return "ACTION"
    return "RAPPORT"

def extract_features(item, valid_words):
    features = set()
    
    # Context features
    ctx = str(item.get('context_analysis', ''))
    if ctx:
        words = re.findall(r'\w+', ctx.lower())
        for w in words:
            if w in valid_words:
                features.add(f"CTX:{w}")
        
    # Reasoning features
    rsn = str(item.get('reasoning_trace', ''))
    if rsn:
        words = re.findall(r'\w+', rsn.lower())
        for w in words:
            if w in valid_words:
                features.add(f"RSN:{w}")

    # Output (HMM State as target)
    pid = item.get('pattern_id', 'UNKNOWN')
    state = get_hmm_state(pid)
    features.add(f"STATE:{state}")
    
    return list(features)

def perform_arm(data, limit=7900):
    valid_words = get_top_words(data[:limit])
    
    print(f"Preparing transactions for {limit} entries...")
    transactions = [extract_features(item, valid_words) for item in tqdm(data[:limit])]
    
    # Filter empty transactions
    transactions = [t for t in transactions if len(t) > 1]
    
    # Encoding
    print(f"Encoding {len(transactions)} transactions...")
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    
    # FP-Growth
    print("Running FP-Growth...")
    frequent_itemsets = fpgrowth(df, min_support=0.05, use_colnames=True)
    
    if frequent_itemsets.empty:
        print("No frequent itemsets found with min_support=0.05")
        return None, None
        
    # Rules
    print("Generating Association Rules...")
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5)
    
    # Filter for rules that lead to STATE
    output_rules = rules[rules['consequents'].apply(lambda x: any('STATE:' in item for item in x))]
    
    return output_rules.sort_values(by='lift', ascending=False), transactions

if __name__ == "__main__":
    src = r'C:\Users\magic\Downloads\erickson_data\augmented_scripts_full.jsonl'
    data = load_data(src)
    
    rules, transactions = perform_arm(data)
    
    if rules is not None and not rules.empty:
        print("\n## Top 20 Association Rules (IF Context/Reasoning THEN Output)")
        # Make rules more readable
        rules['antecedents_str'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
        rules['consequents_str'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))
        
        display_cols = ['antecedents_str', 'consequents_str', 'support', 'confidence', 'lift']
        print(rules[display_cols].head(20).to_string(index=False))
        
        # Save results
        rules.to_csv('erickson_arm_rules_raw.csv', index=False, encoding='utf-8-sig')
        print(f"\nARM analysis saved to erickson_arm_rules_raw.csv")
    else:
        print("No significant rules found.")
