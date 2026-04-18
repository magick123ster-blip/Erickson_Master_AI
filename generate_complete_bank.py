import json
import os
from collections import defaultdict

def generate_full_pattern_bank(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    # Grouping data by pattern_id
    pattern_data = defaultdict(list)
    total_records = 0
    
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
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
    
    report = f"""# 🧠 밀턴 에릭슨 문체 DNA 패턴 뱅크 (V2 - COMPLETE VERSION)

본 문서는 총 **{total_records:,}개**의 모든 증강 데이터를 에릭슨의 핵심 기법별로 분류하여 **누락 없이 전량 수록**한 최종 리포트입니다.

**총 레코드:** {total_records:,}개
**총 고유 패턴:** {num_unique_patterns:,}개

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

## 📂 전 샘플 상세 분석 (All {total_records} Samples)

각 패턴명 하단에 해당 패턴을 사용하는 모든 사례를 수집하였습니다.

""".format(total_records=total_records)

    for pid, samples in sorted_patterns:
        count = len(samples)
        report += f"### 🧩 {pid} (총 {count}개 샘플)\n\n"
        
        # Include EVERY sample (no limit)
        for idx, item in enumerate(samples, 1):
            output = item.get('output', 'N/A')
            instruction = item.get('instruction', 'N/A')
            reasoning = item.get('reasoning_trace', 'N/A')
            
            # Extract topic from context_analysis
            ctx_analysis = item.get('context_analysis', {})
            if isinstance(ctx_analysis, dict):
                context_topic = ctx_analysis.get('topic', 'N/A')
            else:
                context_topic = str(ctx_analysis)
                
            report += f"#### Sample {idx} / {count}\n"
            report += f"> **Output (에릭슨 발화):** \"{output}\"\n\n"
            report += f"- **Instruction (지시어):** {instruction}\n"
            report += f"- **Reasoning Trace (사고 과정):** {reasoning}\n"
            report += f"- **Context:** {context_topic}\n\n"
        
        report += "---\n\n"

    with open(output_file, 'w', encoding='utf-8') as out:
        out.write(report)
        
    print(f"Successfully generated COMPLETED Pattern Bank: {output_file}")
    print(f"File size is roughly {os.path.getsize(output_file) / (1024*1024):.2f} MB")

if __name__ == "__main__":
    base_dir = r"C:\Users\magic\Downloads\erickson_data"
    input_path = os.path.join(base_dir, "augmented_scripts_full.jsonl")
    output_path = os.path.join(base_dir, "erickson_pattern_bank_v2_complete.md")
    generate_full_pattern_bank(input_path, output_path)
