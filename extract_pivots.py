import json
import random

INPUT_FILE = r"C:\Users\magic\Downloads\erickson_data\augmented_scripts_full.jsonl.txt"
OUTPUT_SUMMARY = r"C:\Users\magic\Downloads\erickson_data\pivots_summary.txt"

# Keywords in Korean reasoning to identify a pivot
REASONING_KEYWORDS = ['전환', '우회', '화제', '반전', '맥락을', '흐름을', '비논리', '돌리', '역설', '방향을']

# Linguistic markers in English output that often signal a pivot
# Focus on starting words or strong conjunctives
OUTPUT_MARKERS = ['But ', 'And yet', 'However', 'Now,', 'Well', 'Yes, and', 'By the way', 'So,']

def is_pivot(reasoning, output):
    reasoning_match = any(kw in reasoning for kw in REASONING_KEYWORDS)
    output_match = any(output.strip().startswith(marker) for marker in OUTPUT_MARKERS) or \
                   any(f" {marker} " in output for marker in OUTPUT_MARKERS)
    
    # We want strong evidence of a pivot
    return reasoning_match and output_match

def main():
    pivots = []
    print("Reading data...")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip(): continue
            try:
                record = json.loads(line)
                reasoning = record.get('reasoning_trace', '')
                output = record.get('output', '')
                
                if is_pivot(reasoning, output):
                    pivots.append({
                        'output': output,
                        'reasoning': reasoning
                    })
            except:
                pass
                
    print(f"Found {len(pivots)} potential pivot moments.")
    
    # Take a sample of 30 if there are many, or just save them all
    sample_size = min(30, len(pivots))
    # Using fixed seed for reproducibility so we get consistent examples
    random.seed(42)
    sample_pivots = random.sample(pivots, sample_size)
    
    with open(OUTPUT_SUMMARY, 'w', encoding='utf-8') as out:
        for i, p in enumerate(sample_pivots):
            out.write(f"--- Pivot {i+1} ---\n")
            out.write(f"Output: {p['output']}\n")
            out.write(f"Reasoning: {p['reasoning']}\n\n")
            
    print(f"Saved {sample_size} pivot examples to {OUTPUT_SUMMARY}")

if __name__ == "__main__":
    main()
