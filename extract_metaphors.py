import json
import random

INPUT_FILE = r"C:\Users\magic\Downloads\erickson_data\augmented_scripts_full.jsonl.txt"
OUTPUT_SUMMARY = r"C:\Users\magic\Downloads\erickson_data\metaphors_summary.txt"

# Keywords in Korean reasoning to identify a metaphor/anecdote
REASONING_KEYWORDS = ['은유', '비유', '치환', '투사', '상징', '일화', '이형 동형', '우회적']

def is_metaphor(reasoning, output):
    # Check if reasoning contains metaphor keywords
    return any(kw in reasoning for kw in REASONING_KEYWORDS)

def main():
    metaphors = []
    print("Reading data for metaphors...")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip(): continue
            try:
                record = json.loads(line)
                reasoning = record.get('reasoning_trace', '')
                output = record.get('output', '')
                
                if is_metaphor(reasoning, output) and len(output.split()) > 15: # Metaphors take some length
                    metaphors.append({
                        'output': output,
                        'reasoning': reasoning
                    })
            except Exception as e:
                pass
                
    print(f"Found {len(metaphors)} potential metaphor/anecdote moments.")
    
    # Sort by length or something, or just random sample to get variety
    # Usually stories are longer, so let's pick some of the longer ones, plus some randoms
    metaphors.sort(key=lambda x: len(x['output']), reverse=True)
    
    # Take top 15 longest (good narratives) and 15 randoms from the rest
    top_long = metaphors[:15]
    rest = metaphors[15:]
    random.seed(42)
    sample_rest = random.sample(rest, min(15, len(rest))) if rest else []
    
    final_sample = top_long + sample_rest
    
    with open(OUTPUT_SUMMARY, 'w', encoding='utf-8') as out:
        for i, m in enumerate(final_sample):
            out.write(f"--- Metaphor {i+1} ---\n")
            out.write(f"Output: {m['output'][:800]}...\n") # truncate if too long for readability
            out.write(f"Reasoning: {m['reasoning']}\n\n")
            
    print(f"Saved {len(final_sample)} metaphor examples to {OUTPUT_SUMMARY}")

if __name__ == "__main__":
    main()
