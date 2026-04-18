import json
import os
from collections import Counter, defaultdict

def update_pattern_bank_v2_detailed(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    # Grouping data by pattern_id
    pattern_data = defaultdict(list)
    total_records = 0
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                item = json.loads(line)
                pid = item.get('pattern_id', 'UNKNOWN')
                pattern_data[pid].append(item)
                total_records += 1
            except:
                continue

    # Sorting patterns by frequency
    sorted_patterns = sorted(pattern_data.items(), key=lambda x: len(x[1]), reverse=True)
    num_unique_patterns = len(sorted_patterns)
    
    report = f"""# 🧠 밀턴 에릭슨 문체 DNA 패턴 뱅크 (V2 - Full Detailed Report)

본 문서는 총 **{total_records:,}개**의 증강된 발화 데이터를 기반으로 에릭슨의 핵심 기법 전량을 구조화한 마크다운 리포트입니다.

**총 발견된 고유 패턴 ID:** {num_unique_patterns:,}개

## 📊 패턴 분포 상위 20위

| 패턴 ID | 샘플 수 | 비율 |
| :--- | :--- | :--- |
"""
    for i in range(min(20, num_unique_patterns)):
        pid, samples = sorted_patterns[i]
        count = len(samples)
        percentage = (count / total_records) * 100
        report += f"| {pid} | {count} | {percentage:.1f}% |\n"

    report += """
---

## 📂 대표 패턴 상세 분석 (Top Samples per Pattern)

모든 패턴에 대해 최대 3가지의 대표적인 샘플을 수록하였습니다.

"""
    for pid, samples in sorted_patterns:
        count = len(samples)
        report += f"### 🧩 {pid} (총 {count}개 샘플 존재)\n\n"
        
        # Take top 3 samples
        for idx, item in enumerate(samples[:3], 1):
            output = item.get('output', 'N/A')
            instruction = item.get('instruction', 'N/A')
            reasoning = item.get('reasoning_trace', 'N/A')
            
            # Extract topic from context_analysis
            ctx_analysis = item.get('context_analysis', {})
            if isinstance(ctx_analysis, dict):
                context_topic = ctx_analysis.get('topic', 'N/A')
            else:
                context_topic = str(ctx_analysis)
                
            report += f"#### Sample {idx}\n"
            report += f"> **Output (에릭슨 발화):** \"{output}\"\n\n"
            report += f"- **Instruction (지시어):** {instruction}\n"
            report += f"- **Reasoning Trace (사고 과정):** {reasoning}\n"
            report += f"- **Context:** {context_topic}\n\n"
        
        report += "---\n\n"

    with open(output_file, 'w', encoding='utf-8') as out:
        out.write(report)
        
    print(f"Successfully generated detailed Pattern Bank: {output_file}")

if __name__ == "__main__":
    base_dir = r"C:\Users\magic\Downloads\erickson_data"
    input_path = os.path.join(base_dir, "augmented_scripts_full.jsonl")
    # Using a new name or overwriting the V2 we just made
    output_path = os.path.join(base_dir, "erickson_pattern_bank_v2_detailed.md")
    update_pattern_bank_v2_detailed(input_path, output_path)
