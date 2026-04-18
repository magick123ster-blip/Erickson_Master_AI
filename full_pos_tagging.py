import json
import spacy
import pandas as pd
from tqdm import tqdm

# Load spaCy
print("Loading spaCy model...")
nlp = spacy.load("en_core_web_sm")

def load_data(file_path):
    print(f"Loading data from {file_path}...")
    outputs = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                item = json.loads(line)
                outputs.append(item.get('output', ''))
            except:
                continue
    return outputs

def perform_full_pos_tagging(texts, output_file):
    print(f"Processing {len(texts)} sentences for POS tagging...")
    tagged_data = []
    
    # Use nlp.pipe for efficiency
    for doc in tqdm(nlp.pipe(texts, batch_size=50), total=len(texts)):
        tokens = []
        for token in doc:
            tokens.append({
                "text": token.text,
                "lemma": token.lemma_,
                "pos": token.pos_,
                "tag": token.tag_,
                "dep": token.dep_
            })
        tagged_data.append(tokens)
    
    # Save as JSONL for better structure
    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in tagged_data:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
            
    return tagged_data

if __name__ == "__main__":
    file_path = r'C:\Users\magic\Downloads\erickson_data\augmented_scripts_full.jsonl'
    texts = load_data(file_path)
    
    output_path = 'erickson_pos_tagged_full.jsonl'
    perform_full_pos_tagging(texts, output_path)
    
    print(f"\nPOS tagging complete. Results saved to {output_path}")
