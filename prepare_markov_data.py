import json
import pandas as pd
import glob
import os

# Configuration
DATA_DIR = r'C:\Users\magic\Downloads\erickson_data'
MASTER_CSV = os.path.join(DATA_DIR, 'erickson_master_analysis_data.csv')
OUTPUT_CSV = os.path.join(DATA_DIR, 'erickson_sequences.csv')

# 1. Load Pattern Bank
print("Loading Pattern Bank...")
master_df = pd.read_csv(MASTER_CSV)
# Create a lookup for content -> pattern_id
# We normalize text to avoid minor mismatches
master_df['clean_output'] = master_df['output'].str.strip().str.lower()
pattern_lookup = dict(zip(master_df['clean_output'], master_df['pattern_id']))

# 2. Define High-Level Categorization (Core Patterns)
def map_to_core_pattern(pattern_id):
    if pd.isna(pattern_id):
        return "Unknown"
    
    p = str(pattern_id).lower()
    if "pacing" in p or "rapport" in p or "yes_set" in p:
        return "Pacing"
    if "reframe" in p or "reframing" in p:
        return "Reframing"
    if "utilization" in p:
        return "Utilization"
    if "truism" in p:
        return "Truism"
    if "confusion" in p or "shock" in p or "interrupt" in p:
        return "Confusion"
    if "suggestion" in p or "command" in p or "directive" in p or "association" in p or "future_pace" in p:
        return "Suggestion"
    if "double_bind" in p or "paradox" in p or "illusion_of_choice" in p:
        return "Double Bind"
    
    return "Other"

# 3. Process Script Files
print("Processing Script Files...")
all_script_files = glob.glob(os.path.join(DATA_DIR, "extracted_scripts_*.json"))
sequences = []

for script_path in all_script_files:
    script_id = os.path.basename(script_path).replace("extracted_scripts_", "").replace(".json", "")
    with open(script_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            for i, turn in enumerate(data):
                if turn.get('speaker') == "Milton Erickson":
                    content = str(turn.get('content', '')).strip().lower()
                    pattern_id = pattern_lookup.get(content)
                    
                    if pattern_id:
                        core_label = map_to_core_pattern(pattern_id)
                        sequences.append({
                            "script_id": script_id,
                            "turn_no": i,
                            "content": turn.get('content'),
                            "pattern_id": pattern_id,
                            "pattern_label": core_label
                        })
        except Exception as e:
            print(f"Error processing {script_path}: {e}")

# 4. Save results
seq_df = pd.DataFrame(sequences)
# Filter out "Unknown" or sequences with too few turns if necessary
# In this case, we keep all Milton turns that matched a pattern
seq_df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8-sig')
print(f"Saved {len(seq_df)} turns to {OUTPUT_CSV}")
