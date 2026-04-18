import json
import os
import re
from collections import defaultdict

input_path = r"c:\Users\magic\Downloads\erickson_data\augmented_scripts_full.jsonl"
output_path = r"c:\Users\magic\Downloads\erickson_data\hypnotic_pattern_db.json"

# 기법 그룹화 맵핑 (Broad categories mapping)
CATEGORY_MAP = {
    "DOUBLE_BIND": ["DOUBLE_BIND", "TRIVIAL_CHOICE", "ILLUSORY_CHOICE", "BIND"],
    "TEMPORAL": ["TEMPORAL", "AGE_REGRESSION", "AGE_PROGRESSION", "FUTURE_PACING", "REVIVIFICATION", "HISTORY"],
    "SUGGESTION": ["INDIRECT_SUGGESTION", "DIRECT_SUGGESTION", "EMBEDDED", "INSTRUCTION", "AUTHORITY", "METAPHOR", "ANALOGY"],
    "DISSOCIATION": ["DISSOCIATION", "AMNESIA", "SPLIT", "DISSOCIATIVE", "AWARENESS_SHIFT"],
    "UTILIZATION": ["UTILIZATION", "UTILISATION", "REFRAMING", "REFRAME", "ACCEPTANCE", "PACING"],
    "IDEOMOTOR": ["IDEOMOTOR", "CATALEPSY", "PHYSIOLOGICAL", "LEVITATION", "MOTOR", "SENSORIMOTOR"],
    "TRUISM": ["TRUISM", "YES_SET", "YESSET", "FACTUAL", "UNIVERSAL"]
}

def get_category(pattern_id):
    pid = pattern_id.upper()
    for cat, markers in CATEGORY_MAP.items():
        if any(marker in pid for marker in markers):
            return cat
    return "OTHER"

def extract_patterns():
    db = defaultdict(list)
    counts = defaultdict(int)
    
    print(f"Reading {input_path}...")
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                pid = data.get('pattern_id', 'UNKNOWN')
                cat = get_category(pid)
                
                # 데이터 정제 및 샘플 보관
                sample = {
                    "id": pid,
                    "eng": data.get('output', ''),
                    "reasoning": data.get('reasoning_trace', ''),
                    "context": data.get('context_analysis', {}).get('topic', '')
                }
                
                db[cat].append(sample)
                counts[cat] += 1
            except Exception as e:
                continue

    # 최종 결과 정리 (기법당 상위 5개씩만 유지 및 핵심 로직 요약)
    final_db = {}
    for cat, samples in db.items():
        if cat == "OTHER": continue
        
        # 중복 제거 및 간단한 정렬 (긴 문장 중심)
        unique_samples = []
        seen_eng = set()
        for s in sorted(samples, key=lambda x: len(x['eng']), reverse=True):
            if s['eng'] not in seen_eng:
                unique_samples.append(s)
                seen_eng.add(s['eng'])
            if len(unique_samples) >= 5:
                break
        
        final_db[cat] = {
            "count": counts[cat],
            "samples": unique_samples
        }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_db, f, ensure_ascii=False, indent=2)
    
    print(f"Extraction complete. DB saved to {output_path}")
    print("Category Stats:", dict(counts))

if __name__ == "__main__":
    extract_patterns()
