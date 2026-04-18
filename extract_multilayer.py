import json
import random

INPUT_FILE = r"C:\Users\magic\Downloads\erickson_data\augmented_scripts_full.jsonl.txt"
OUTPUT_SUMMARY = r"C:\Users\magic\Downloads\erickson_data\training_multilayer_full.jsonl"

# Keywords in Korean reasoning to identify multi-layer / hidden message mechanisms
REASONING_KEYWORDS = ['표면적', '숨겨진', '이중 구속', '내장된 명령', '다중 메시지', '레이어', '의식은', '무의식은', '이중적', '암시', '포장']

def is_multilayer(reasoning, output):
    # Check if reasoning contains multilayer keywords
    count = sum(1 for kw in REASONING_KEYWORDS if kw in reasoning)
    return count >= 2  # Require at least 2 keywords for stronger confidence of structural depth

def main():
    multilayers = []
    print("Reading data for multi-layer stacking...")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip(): continue
            try:
                record = json.loads(line)
                reasoning = record.get('reasoning_trace', '')
                output = record.get('output', '')
                
                if is_multilayer(reasoning, output) and len(output.split()) > 10: 
                    multilayers.append({
                        'output': output,
                        'reasoning': reasoning
                    })
            except Exception as e:
                pass
                
    print(f"Found {len(multilayers)} potential multi-layer stacking moments.")
    
    # No random sampling, we want all 255+ items for training
    
    with open(OUTPUT_SUMMARY, 'w', encoding='utf-8') as out:
        for m in multilayers:
            out.write(json.dumps(m, ensure_ascii=False) + '\n')
            
    print(f"Saved {len(multilayers)} full multilayer examples to {OUTPUT_SUMMARY}")

if __name__ == "__main__":
    main()
