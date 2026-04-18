import json
import csv
import os
from collections import defaultdict, Counter

def distill_data(input_file, output_prefix, target_count=1500):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    data = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                item = json.loads(line)
                # 계산 기반: Reasoning Trace 길이 + Output 품질 등 가상의 점수 부여
                reasoning_len = len(item.get('reasoning_trace', ''))
                output_len = len(item.get('output', ''))
                
                # 점수 산정 (사고 과정이 길고 구체적일수록 높은 가중치)
                score = (reasoning_len * 1.5) + output_len
                item['distill_score'] = score
                data.append(item)
            except:
                continue

    # 1. 패턴별로 그룹화
    pattern_groups = defaultdict(list)
    for item in data:
        pattern_groups[item['pattern_id']].append(item)

    # 2. 각 패턴 내에서 점수가 높은 순으로 정렬
    for pid in pattern_groups:
        pattern_groups[pid].sort(key=lambda x: x['distill_score'], reverse=True)

    # 3. 데이터 선정 (Round-robin 방식: 모든 패턴을 골고루 포함하면서 고득점자 위주)
    essential_data = []
    pids = sorted(pattern_groups.keys(), key=lambda p: len(pattern_groups[p]), reverse=True)
    
    # 넉넉하게 반복하며 채우기
    for i in range(100): # 각 패턴별 최대 100개까지 시도
        if len(essential_data) >= target_count:
            break
        for pid in pids:
            if i < len(pattern_groups[pid]):
                essential_data.append(pattern_groups[pid][i])
                if len(essential_data) >= target_count:
                    break

    # 4. 결과 저장
    csv_output = f"{output_prefix}_essential_{target_count}.csv"
    jsonl_output = f"{output_prefix}_essential_{target_count}.jsonl"

    headers = ["input_text", "output_text"]
    records = []
    for item in essential_data:
        prompt = f"지시: {item.get('instruction', '')}\n문맥: {item.get('context_analysis', {}).get('topic', '')}"
        response = f"사고 과정: {item.get('reasoning_trace', '')}\n에릭슨 발화: {item.get('output', '')}"
        records.append({"input_text": prompt, "output_text": response})

    with open(csv_output, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(records)

    with open(jsonl_output, 'w', encoding='utf-8') as f:
        for item in essential_data:
            prompt = f"지시: {item.get('instruction', '')}\n문맥: {item.get('context_analysis', {}).get('topic', '')}"
            response = f"사고 과정: {item.get('reasoning_trace', '')}\n에릭슨 발화: {item.get('output', '')}"
            chat_obj = {
                "contents": [
                    {"role": "user", "parts": [{"text": prompt}]},
                    {"role": "model", "parts": [{"text": response}]}
                ]
            }
            f.write(json.dumps(chat_obj, ensure_ascii=False) + "\n")

    print(f"✅ 정제된 데이터셋 생성 완료! (총 {len(essential_data)}개)")
    print(f"  - CSV: {csv_output}")
    print(f"  - JSONL: {jsonl_output}")

if __name__ == "__main__":
    import sys
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')

    src = r"C:\Users\magic\Downloads\erickson_data\augmented_scripts_full.jsonl"
    dst_prefix = r"C:\Users\magic\Downloads\erickson_data\erickson_tuning"
    distill_data(src, dst_prefix, 1500)
