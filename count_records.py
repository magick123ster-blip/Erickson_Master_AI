import json
import glob
import os

def count():
    base_dir = r"C:\Users\magic\Downloads\erickson_data"
    json_files = glob.glob(os.path.join(base_dir, "extracted_scripts_*.json"))
    
    total_json_lines = 0
    for f in json_files:
        try:
            with open(f, 'r', encoding='utf-8', errors='ignore') as jf:
                data = json.load(jf)
                total_json_lines += len(data)
        except Exception as e:
            print(f"Error reading {f}: {e}")
            
    jsonl_file = os.path.join(base_dir, "augmented_scripts_full.jsonl")
    total_jsonl_lines = 0
    if os.path.exists(jsonl_file):
        with open(jsonl_file, 'r', encoding='utf-8', errors='ignore') as jlf:
            total_jsonl_lines = sum(1 for line in jlf if line.strip())
            
    print(f"Total extracted script lines (JSON): {total_json_lines}")
    print(f"Total augmented script lines (JSONL): {total_jsonl_lines}")
    print(f"Remaining: {total_json_lines - total_jsonl_lines}")

if __name__ == "__main__":
    count()
