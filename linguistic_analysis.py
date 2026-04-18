import json
import spacy
from collections import Counter

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

def load_data(file_path):
    outputs = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                item = json.loads(line)
                outputs.append(item.get('output', ''))
            except:
                continue
    return outputs

def analyze_linguistics(texts):
    print(f"Analyzing {len(texts)} script entries...")
    
    suggestive_verbs = ["wonder", "discover", "notice", "allow", "permit", "find", "begin", "realize", "learn", "feel"]
    verb_counts = Counter()
    passive_count = 0
    double_bind_conjunctions = ["either", "or", "whether"]
    conj_counts = Counter()
    
    # Analyze a subset for performance if needed, but let's try the whole set first
    # Or just analyze top N for speed if the file is massive
    for doc in nlp.pipe(texts, batch_size=50):
        # 1. Suggestive Verbs
        for token in doc:
            if token.lemma_.lower() in suggestive_verbs and token.pos_ == "VERB":
                verb_counts[token.lemma_.lower()] += 1
            
            # 2. Passive Voice (Subject-less or Indirect)
            # Simplified check: auxiliary verb + past participle + passive subject dependency
            if token.dep_ == "auxpass":
                passive_count += 1
                
            # 3. Double Bind Conjunctions
            if token.text.lower() in double_bind_conjunctions:
                conj_counts[token.text.lower()] += 1

    return verb_counts, passive_count, conj_counts

if __name__ == "__main__":
    file_path = r'C:\Users\magic\Downloads\erickson_data\augmented_scripts_full.jsonl'
    texts = load_data(file_path)
    
    # To avoid excessive processing time for this specific task, let's process a significant sample
    sample_size = 2000
    texts_sample = texts[:sample_size]
    
    verbs, passive, conjs = analyze_linguistics(texts_sample)
    
    print("\n## Linguistic Analysis Results (Sample Size: 2000)")
    
    print("\n### 1. Suggestive Verbs (Prompting Internal Search)")
    for verb, count in verbs.most_common():
        print(f"- {verb}: {count}")
        
    print("\n### 2. Passive Voice / Accountability Shifting")
    print(f"- Total Passive Structures Found: {passive}")
    print(f"- Frequency: {passive/sample_size*100:.1f}% of segments contains passive voice")
    
    print("\n### 3. Therapeutic Choice (Double Bind Conjunctions)")
    for conj, count in conjs.most_common():
        print(f"- {conj}: {count}")
