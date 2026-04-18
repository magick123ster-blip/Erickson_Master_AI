import json
import os
from collections import Counter, defaultdict

def update_pattern_bank(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    patterns = Counter()
    category_map = defaultdict(list)
    
    # We want to keep the report structure but refresh the numbers
    total_records = 0
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                item = json.loads(line)
                pid = item.get('pattern_id', 'UNKNOWN')
                patterns[pid] += 1
                total_records += 1
            except:
                continue

    top_20 = patterns.most_common(20)
    
    report = f"""# 📊 Milton Erickson DNA Pattern Bank (V2 - Full Dataset)

본 문서는 **총 {total_records:,}개**의 에릭슨 커뮤니케이션 레코드를 전수 분석한 결과입니다. 
기존의 파편화된 데이터에서 벗어나, 에릭슨의 모든 발화 패턴을 통계적으로 구조화했습니다.

## 1. 데이터셋 요약
*   **분석 대상:** `augmented_scripts_full.jsonl`
*   **총 레코드 수:** {total_records:,} 개
*   **고유 패턴 식별:** {len(patterns):,} 종류

## 2. 상위 20개 핵심 패턴 분포
에릭슨이 가장 빈번하게 사용한 상위 20개 패턴입니다.

| 순위 | 패턴 ID | 빈도수 | 비율 (%) |
| :--- | :--- | :--- | :--- |
"""
    for i, (pid, count) in enumerate(top_20, 1):
        percentage = (count / total_records) * 100
        report += f"| {i} | `{pid}` | {count:,} | {percentage:.2f}% |\n"

    report += """
## 3. 전체 패턴 인덱스 (Full Index)
모든 식별된 패턴의 빈도 리스트입니다.

"""
    all_patterns = patterns.most_common()
    for pid, count in all_patterns:
        report += f"*   `{pid}`: {count:,} 회\n"

    with open(output_file, 'w', encoding='utf-8') as out:
        out.write(report)
        
    print(f"Successfully updated Pattern Bank: {output_file}")

if __name__ == "__main__":
    base_dir = r"C:\Users\magic\Downloads\erickson_data"
    input_path = os.path.join(base_dir, "augmented_scripts_full.jsonl")
    output_path = os.path.join(base_dir, "erickson_pattern_bank_v2.md")
    update_pattern_bank(input_path, output_path)
