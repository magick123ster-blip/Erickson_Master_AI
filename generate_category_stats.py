import json
import os
from collections import defaultdict, Counter

def categorize_pattern(pid):
    pid_upper = pid.upper()
    if "UTILIZATION" in pid_upper:
        return "Utilization (활용)"
    elif "REFRAME" in pid_upper or "REFRAMING" in pid_upper:
        return "Reframing (재구성)"
    elif "SUGGESTION" in pid_upper:
        return "Suggestions (암시 기법)"
    elif "TRUISM" in pid_upper or "PACING" in pid_upper:
        return "Pacing & Truisms (보편적 사실/보조 맞추기)"
    elif "DISSOCIATION" in pid_upper:
        return "Dissociation (분리 기법)"
    elif "DOUBLE_BIND" in pid_upper or "PARADOX" in pid_upper:
        return "Double Binds & Paradox (이중 구속/역설)"
    elif "METAPHOR" in pid_upper or "ANALOGY" in pid_upper or "STORY" in pid_upper:
        return "Metaphors & Symbolic (은유/상징)"
    elif "AMBIGUITY" in pid_upper or "CONFUSION" in pid_upper:
        return "Ambiguity & Confusion (모호함/혼란)"
    else:
        return "Other Erickson Techniques (기타 기법)"

def generate_category_stats(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    category_counts = Counter()
    pattern_within_category = defaultdict(Counter)
    total_records = 0
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                item = json.loads(line)
                pid = item['pattern_id']
                cat = categorize_pattern(pid)
                
                category_counts[cat] += 1
                pattern_within_category[cat][pid] += 1
                total_records += 1
            except:
                continue
                
    if total_records == 0:
        print("No valid records found.")
        return

    # Sort categories by size
    sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
    
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write("# 📂 밀턴 에릭슨 기법 카테고리별 분류 및 분포 리포트\n\n")
        out.write(f"본 리포트는 총 **{total_records}건**의 증강된 발화 데이터를 대분류(Category) 단위로 구조화한 결과입니다.\n\n")
        
        out.write("## 📊 대분류별 비중\n\n")
        out.write("| 순위 | 카테고리명 | 샘플 수 | 비율(%) |\n")
        out.write("| :--- | :--- | :--- | :--- |\n")
        for i, (cat, count) in enumerate(sorted_categories):
            pct = (count / total_records) * 100
            out.write(f"| {i+1} | {cat} | {count} | {pct:.2f}% |\n")
            
        out.write("\n---\n\n")
        
        out.write("## 🔍 카테고리별 세부 패턴 분포 (Top 10 Patterns per Category)\n\n")
        for cat, _ in sorted_categories:
            cat_total = category_counts[cat]
            out.write(f"### 📁 {cat} (전체의 {cat_total/total_records*100:.1f}%)\n\n")
            out.write(f"해당 카테고리에 속한 상위 10개 세부 패턴입니다.\n\n")
            out.write("| 패턴 ID | 빈도수 | 카테고리 내 비율 |\n")
            out.write("| :--- | :--- | :--- |\n")
            
            top_patterns = pattern_within_category[cat].most_common(10)
            for pid, count in top_patterns:
                out.write(f"| {pid} | {count} | {count/cat_total*100:.1f}% |\n")
            out.write("\n")

    print(f"Category statistics report created at: {output_file}")

if __name__ == "__main__":
    src = r"C:\Users\magic\Downloads\erickson_data\augmented_scripts_full.jsonl"
    dst = r"C:\Users\magic\Downloads\erickson_data\erickson_category_distribution.md"
    
    import sys
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
        
    generate_category_stats(src, dst)
