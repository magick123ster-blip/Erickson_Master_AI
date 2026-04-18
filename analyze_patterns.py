import json
from collections import Counter

file_path = r'C:\Users\magic\Downloads\erickson_data\augmented_scripts_full.jsonl'
ids = []

with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            ids.append(data.get('pattern_id', 'UNKNOWN'))
        except Exception as e:
            print(f"Error parsing line: {e}")

counts = Counter(ids)
for pid, count in counts.most_common():
    print(f"{pid}: {count}")
