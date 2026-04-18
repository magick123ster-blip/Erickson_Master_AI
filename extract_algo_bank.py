import json
import re
from collections import Counter, defaultdict

data_path = r"C:\Users\magic\Downloads\erickson_data\augmented_scripts_full.jsonl.TXT"

def extract_algorithm_bank(file_path):
    algorithms = {
        'double_bind': [], # Logic of choice
        'temporal_displacement': [], # Past/Future/Now shifting
        'negative_suggestion': [], # "Don't" usage
        'nominalization_ambiguity': [], # Abstract nouns
        'embedded_commands': [], # Interspersal
        'ideomotor_linking': [] # Thought-body links
    }
    
    counts = Counter()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip(): continue
                item = json.loads(line)
                output = item.get('output', '')
                output_l = output.lower()
                
                # 1. Double Bind (Either/Or choice that leads to same goal)
                if re.search(r'\b(either|or|whether|choice)\b', output_l) and '?' in output_l:
                    algorithms['double_bind'].append({'t': output, 'p': item.get('pattern_id')})
                
                # 2. Temporal Displacement (Age regression/Future pacing)
                if re.search(r'\b(remember|forget|past|future|years|time|when you were|will be)\b', output_l):
                    algorithms['temporal_displacement'].append({'t': output, 'p': item.get('pattern_id')})
                
                # 3. Negative Suggestion (Reverse)
                if re.search(r'\b(don\'t|not|stop|trying)\b', output_l) and any(v in output_l for v in ['want', 'need', 'have to', 'necessary']):
                    algorithms['negative_suggestion'].append({'t': output, 'p': item.get('pattern_id')})
                
                # 4. Nominalization (Abstract nouns that lack concrete referents)
                # Words like learning, knowledge, unconscious, curiosity, etc.
                if re.search(r'\b(learning|knowledge|curiosity|comfort|awareness|understanding)\b', output_l):
                    algorithms['nominalization_ambiguity'].append({'t': output, 'p': item.get('pattern_id')})

                # 5. Embedded Commands (Often inside quotes or "i want you to")
                if re.search(r'\b(i want you to|you might notice|you may find)\b', output_l):
                    algorithms['embedded_commands'].append({'t': output, 'p': item.get('pattern_id')})
                
                # 6. Ideomotor Linking (Hand, foot, movement + thinking)
                if re.search(r'\b(hand|foot|lifting|moving|finger|twitch)\b', output_l) and re.search(r'\b(thinking|noticing|knowing)\b', output_l):
                    algorithms['ideomotor_linking'].append({'t': output, 'p': item.get('pattern_id')})

        # Keep top 15 samples for each to avoid bloat
        result = {}
        for k, v in algorithms.items():
            result[k] = v[:15]
            counts[k] = len(v)
            
        return {'data': result, 'stats': dict(counts)}
        
    except Exception as e:
        return {'error': str(e)}

if __name__ == "__main__":
    try:
        report_data = extract_algorithm_bank(data_path)
        with open(r"C:\Users\magic\Downloads\erickson_data\algo_bank_results.json", "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        print("Algorithm Bank Extraction Complete.")
    except Exception as e:
        print(f"Error: {e}")
