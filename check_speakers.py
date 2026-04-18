import glob
import json
import os

DATA_DIR = r'C:\Users\magic\Downloads\erickson_data'
all_script_files = glob.glob(os.path.join(DATA_DIR, "extracted_scripts_*.json"))

speakers = {}

for script_path in all_script_files:
    with open(script_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for turn in data:
            speaker = turn.get('speaker', 'Unknown')
            speakers[speaker] = speakers.get(speaker, 0) + 1

print("Speakers found:")
for k, v in sorted(speakers.items(), key=lambda item: item[1], reverse=True):
    print(f"{k}: {v}")
