import json
import os
from collections import Counter

def generate_pattern_stats(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    pattern_counts = Counter()
    total_records = 0
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                item = json.loads(line)
                pattern_counts[item['pattern_id']] += 1
                total_records += 1
            except:
                continue
                
    if total_records == 0:
        print("No valid records found.")
        return

    # Sort patterns by frequency
    sorted_patterns = pattern_counts.most_common()
    
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write("# 📊 밀턴 에릭슨 기법별 사용 빈도 및 분포 리포트\n\n")
        out.write(f"본 리포트는 총 **{total_records}건**의 증강된 발화 데이터를 분석한 결과입니다.\n\n")
        
        out.write("## 📌 요약 테이블\n\n")
        out.write("| 순위 | 패턴 ID (기법명) | 빈도수 | 비율(%) | 누적 비율 |\n")
        out.write("| :--- | :--- | :--- | :--- | :--- |\n")
        
        cumulative_pct = 0
        for i, (pid, count) in enumerate(sorted_patterns):
            pct = (count / total_records) * 100
            cumulative_pct += pct
            out.write(f"| {i+1} | {pid} | {count} | {pct:.2f}% | {cumulative_pct:.2f}% |\n")
            
    print(f"Statistics report created at: {output_file}")

if __name__ == "__main__":
    src = r"C:\Users\magic\Downloads\erickson_data\augmented_scripts_full.jsonl"
    dst = r"C:\Users\magic\Downloads\erickson_data\erickson_pattern_distribution.md"
    generate_pattern_stats(src, dst)
