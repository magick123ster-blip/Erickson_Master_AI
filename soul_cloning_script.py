import json
import re
from collections import Counter, defaultdict

data_path = r"C:\Users\magic\Downloads\erickson_data\augmented_scripts_full.jsonl.TXT"

def soul_cloning_analysis(file_path):
    micro_moves = Counter()
    linguistic_structures = Counter()
    psychological_triggers = Counter()
    
    # Specific connectors and modifiers
    connectors = Counter()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip(): continue
                try:
                    item = json.loads(line)
                    output = item.get('output', '').lower()
                    reasoning = item.get('reasoning_trace', '')
                    
                    # 1. Extract Micro-Moves from Reasoning (Korean)
                    # Look for intent verbs and nouns
                    moves = re.findall(r'\b(우회|혼란|해리|추인|암시|활용|전제|이중 구속|관념운동|동기 부여|자원 인출|강화|연결|페이싱|리딩)\b', reasoning)
                    for move in moves:
                        micro_moves[move] += 1
                        
                    # 2. Extract Psychological Triggers from Reasoning
                    triggers = re.findall(r'\b(의식적 저항|비판적 사고|무의식적 반응|내적 탐색|고착된 관념|학습된 능력|잠재력)\b', reasoning)
                    for trigger in triggers:
                        psychological_triggers[trigger] += 1
                        
                    # 3. Linguistic Structures (English output)
                    # Check for conditional/indirect structures
                    if re.search(r'\b(if|when|as)\b.*\b(then|would|could|can)\b', output):
                        linguistic_structures['conditional_leading'] += 1
                    if re.search(r'\b(i wonder|i don\'t know|perhaps|maybe)\b', output):
                        linguistic_structures['permissive_uncertainty'] += 1
                    if re.search(r'\b(conscious|unconscious|mind|thought)\b', output):
                        linguistic_structures['egological_split'] += 1
                    if re.search(r'\b(suppose|imagine|pretend)\b', output):
                        linguistic_structures['hypothetical_immersion'] += 1
                    
                    # 4. Sentence Openers (Connectors)
                    first_two_words = ' '.join(re.findall(r'\b\w+\b', output)[:2])
                    if first_two_words:
                        connectors[first_two_words] += 1

                except json.JSONDecodeError: continue

        return {
            'micro_moves': micro_moves.most_common(20),
            'psychological_triggers': psychological_triggers.most_common(20),
            'linguistic_structures': dict(linguistic_structures),
            'common_openers': connectors.most_common(30)
        }
        
    except Exception as e:
        return {'error': str(e)}

if __name__ == "__main__":
    results = soul_cloning_analysis(data_path)
    print(json.dumps(results, indent=2, ensure_ascii=False))
