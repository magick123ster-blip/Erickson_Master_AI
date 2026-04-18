import json
import re
from collections import Counter, defaultdict

data_path = r"C:\Users\magic\Downloads\erickson_data\augmented_scripts_full.jsonl.TXT"

def deep_linguistic_analysis(file_path):
    patterns = []
    reasoning_texts = []
    output_texts = []
    context_topics = []
    
    # Transition mapping
    transitions = defaultdict(Counter)
    last_pattern = None
    
    # N-gram mapping
    trigrams = Counter()
    
    # Strategic Triplet (Concept clustering)
    concept_triplets = Counter()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip(): continue
                try:
                    item = json.loads(line)
                    
                    pattern_id = item.get('pattern_id', 'UNKNOWN').replace('ERICKSON_', '')
                    output = item.get('output', '').lower()
                    reasoning = item.get('reasoning_trace', '')
                    context = item.get('context_analysis', {}).get('topic', '')
                    
                    patterns.append(pattern_id)
                    output_texts.append(output)
                    reasoning_texts.append(reasoning)
                    context_topics.append(context)
                    
                    # 1. Transitions
                    if last_pattern:
                        transitions[last_pattern][pattern_id] += 1
                    last_pattern = pattern_id
                    
                    # 2. Trigrams (3-word sequences)
                    words = re.findall(r'\b\w+\b', output)
                    for i in range(len(words)-2):
                        tri = tuple(words[i:i+3])
                        trigrams[tri] += 1
                        
                    # 3. Strategic Triplets in Reasoning (Keywords cluster)
                    # Extract 3 non-stopword keywords from reasoning to find "concept clusters"
                    r_words = re.findall(r'\b\w{4,}\b', reasoning.lower())
                    stop_concepts = ['내담자', '대한', '통해', '수', '의', '에', '을', '를', '이', '가'] # Basic Korean stops
                    filtered_r = [w for w in r_words if w not in stop_concepts]
                    if len(filtered_r) >= 3:
                        for i in range(len(filtered_r)-2):
                            concept_triplets[tuple(filtered_r[i:i+3])] += 1

                except json.JSONDecodeError: continue

        # Summarize Transitions
        top_transitions = []
        for p, counts in transitions.items():
            best_next = counts.most_common(1)
            if best_next and counts[best_next[0][0]] > 5: # Significant transitions
                top_transitions.append((p, best_next[0][0], best_next[0][1]))
        
        top_transitions.sort(key=lambda x: x[2], reverse=True)

        return {
            'top_trigrams': [(' '.join(k), v) for k, v in trigrams.most_common(30)],
            'technique_transitions': top_transitions[:20],
            'concept_clusters': [(':'.join(k), v) for k, v in concept_triplets.most_common(20)],
            'thematic_keywords': Counter([w for text in context_topics for w in re.findall(r'\b\w{2,}\b', text)]).most_common(20)
        }
        
    except Exception as e:
        return {'error': str(e)}

if __name__ == "__main__":
    results = deep_linguistic_analysis(data_path)
    print(json.dumps(results, indent=2, ensure_ascii=False))
