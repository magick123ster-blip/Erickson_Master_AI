import json
import re

data_path = r"C:\Users\magic\Downloads\erickson_data\augmented_scripts_full.jsonl.TXT"

def extract_rule_evidence(file_path):
    rule1_samples = [] # Egological Split
    rule2_samples = [] # Conditional Leading
    rule3_samples = [] # Permissive Uncertainty
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip(): continue
                item = json.loads(line)
                output = item.get('output', '')
                output_l = output.lower()
                
                # Rule 1: Egological Split
                if 'conscious' in output_l and 'unconscious' in output_l:
                    rule1_samples.append({
                        'text': output,
                        'pattern': item.get('pattern_id'),
                        'reasoning': item.get('reasoning_trace')
                    })
                
                # Rule 2: Conditional Leading
                if re.search(r'\b(as|when|while)\b\s+you', output_l) and re.search(r'\b(then|will|would|could|can)\b', output_l):
                    rule2_samples.append({
                        'text': output,
                        'pattern': item.get('pattern_id'),
                        'reasoning': item.get('reasoning_trace')
                    })
                
                # Rule 3: Permissive Uncertainty
                if re.search(r'\b(wonder|not know|don\'t know|perhaps|maybe)\b', output_l):
                    rule3_samples.append({
                        'text': output,
                        'pattern': item.get('pattern_id'),
                        'reasoning': item.get('reasoning_trace')
                    })
                    
        return {
            'rule1': rule1_samples[:10],
            'rule2': rule2_samples[:10],
            'rule3': rule3_samples[:10],
            'stats': {
                'rule1_count': len(rule1_samples),
                'rule2_count': len(rule2_samples),
                'rule3_count': len(rule3_samples)
            }
        }
    except Exception as e:
        return {'error': str(e)}

if __name__ == "__main__":
    try:
        results = extract_rule_evidence(data_path)
        with open(r"C:\Users\magic\Downloads\erickson_data\rule_evidence_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print("Analysis complete. Results written to rule_evidence_results.json")
    except Exception as e:
        print(f"Error: {str(e)}")
