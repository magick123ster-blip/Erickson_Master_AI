import pandas as pd
import json
import os

def prepare_dataset():
    print("Loading sequence data (CSV)...")
    csv_path = 'erickson_sequences_with_submacros.csv'
    jsonl_path = 'augmented_scripts_full.jsonl'
    output_path = 'erickson_deep_learning_dataset.jsonl'
    
    df_seq = pd.read_csv(csv_path)
    
    print("Loading augmented data (JSONL)...")
    augmented_data = []
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            augmented_data.append(json.loads(line))
            
    # Step 1: Align CSV and JSONL
    # Since they are aligned by order but CSV has fewer rows (only patterned turns), 
    # we match them based on the 'content' in CSV and 'output' in JSONL.
    
    merged_data = []
    aug_idx = 0
    total_aug = len(augmented_data)
    
    print("Merging datasets based on content alignment...")
    for idx, row in df_seq.iterrows():
        content = str(row['content']).strip().lower()
        
        # Search for matching output in JSONL starting from current aug_idx
        matched = False
        # We search a bit ahead in case of minor offsets
        for search_idx in range(aug_idx, min(aug_idx + 50, total_aug)):
            aug_item = augmented_data[search_idx]
            aug_output = str(aug_item['output']).strip().lower()
            
            if content in aug_output or aug_output in content:
                item = {
                    'script_id': row['script_id'],
                    'turn_no': row['turn_no'],
                    'pattern_id': row['pattern_id'],
                    'macro': row['macro'],
                    'sub_macro': row['sub_macro'],
                    'reasoning': aug_item['reasoning_trace'],
                    'output_text': aug_item['output'],
                    'instruction': aug_item['instruction']
                }
                merged_data.append(item)
                aug_idx = search_idx + 1
                matched = True
                break
                
    print(f"Successfully merged {len(merged_data)} turns.")
    
    # Step 2: Create Sequences (Sliding Window of 5)
    final_dataset = []
    window_size = 5
    
    print(f"Generating sequences with window size {window_size}...")
    # Group by script to ensure sequences don't cross boundaries
    merged_df = pd.DataFrame(merged_data)
    for script_id, group in merged_df.groupby('script_id'):
        group = group.sort_values('turn_no')
        patterns = group['pattern_id'].tolist()
        reasonings = group['reasoning'].tolist()
        outputs = group['output_text'].tolist()
        macros = group['macro'].tolist()
        
        for i in range(len(patterns)):
            # History is previous pattern IDs
            history = patterns[max(0, i - window_size):i]
            history_str = " -> ".join(history) if history else "START"
            
            target_pattern = patterns[i]
            target_reasoning = reasonings[i]
            target_output = outputs[i]
            target_macro = macros[i]
            
            entry = {
                "instruction": "Milton Erickson's Strategic Intervention Simulation",
                "input": f"Conversation History (Patterns): [{history_str}]. Current Strategic Goal: {target_macro}.",
                "output": f"### Chosen Pattern: {target_pattern}\n\n### Reasoning Trace:\n{target_reasoning}\n\n### Erickson's Response:\n{target_output}"
            }
            final_dataset.append(entry)
            
    # Save final dataset
    with open(output_path, 'w', encoding='utf-8') as f:
        for entry in final_dataset:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
            
    print(f"Final dataset saved to {output_path} ({len(final_dataset)} entries).")

if __name__ == "__main__":
    prepare_dataset()
