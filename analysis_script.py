import json
import re
from collections import Counter

# File path
data_path = r"C:\Users\magic\Downloads\erickson_data\augmented_scripts_full.jsonl.TXT"

def analyze_erickson_data(file_path):
    pattern_counts = Counter()
    total_lines = 0
    modal_verbs_counts = Counter()
    modal_verbs = ['may', 'might', 'could', 'can', 'should', 'would', 'suppose']
    
    sentence_types = {
        'questions': 0,
        'imperatives': 0,
        'declaratives': 0
    }
    
    keywords = Counter()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    item = json.loads(line)
                    total_lines += 1
                    
                    # Pattern counts
                    pattern_id = item.get('pattern_id', 'UNKNOWN')
                    # Strip ERICKSON_ prefix for cleaner labels
                    clean_pattern = pattern_id.replace('ERICKSON_', '')
                    pattern_counts[clean_pattern] += 1
                    
                    # Output text analysis
                    output_text = item.get('output', '').lower()
                    
                    # 1. Modal verbs
                    for verb in modal_verbs:
                        if re.search(rf'\b{verb}\b', output_text):
                            modal_verbs_counts[verb] += 1
                            
                    # 2. Sentence types
                    if '?' in output_text:
                        sentence_types['questions'] += 1
                    
                    # Simplified imperative check (starts with verb or contains please/don't)
                    # This is a heuristic for hypnotic suggestions
                    if any(output_text.strip().startswith(v) for v in ['tell', 'just', 'go', 'close', 'let', 'open', 'listen', 'focus', 'keep']):
                        sentence_types['imperatives'] += 1
                    else:
                        sentence_types['declaratives'] += 1
                        
                    # 3. Keyword extraction (simple tokenization)
                    tokens = re.findall(r'\b\w{4,}\b', output_text) # long enough words
                    for token in tokens:
                        if token not in ['your', 'that', 'with', 'this', 'have', 'from', 'what', 'when', 'into']:
                            keywords[token] += 1
                            
                except json.JSONDecodeError:
                    continue
                    
        return {
            'total_samples': total_lines,
            'top_patterns': pattern_counts.most_common(20),
            'modal_verbs': modal_verbs_counts.most_common(),
            'sentence_distribution': sentence_types,
            'top_keywords': keywords.most_common(30)
        }
        
    except Exception as e:
        return {'error': str(e)}

if __name__ == "__main__":
    results = analyze_erickson_data(data_path)
    print(json.dumps(results, indent=2))
