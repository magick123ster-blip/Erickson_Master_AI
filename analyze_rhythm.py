import json
import pandas as pd
import numpy as np
import re

INPUT_JSONL = r"C:\Users\magic\Downloads\erickson_data\augmented_scripts_full.jsonl.txt"
INPUT_CSV = r"C:\Users\magic\Downloads\erickson_data\erickson_strategy_clusters.csv"
OUTPUT_TXT = r"C:\Users\magic\Downloads\erickson_data\rhythm_analysis_results.txt"

CLUSTER_NAMES = {
    0: "결핍의 치명적 자산화",
    1: "시간적 지연과 과정의 유예",
    2: "부정적 예스-세트",
    3: "문제의 기술적 해체",
    4: "우회적 성취 루프",
    5: "저항의 역설적 과제화",
    6: "기억 단절을 위한 일상적 닻",
    7: "데이터 기반의 논리 폭파",
    8: "허용적 전제 질문법",
    9: "학술/역사적 닻 내리기",
    10: "최소 개입 페이싱",
    11: "증상 소유권 부여",
    12: "일상 감각의 메타포화",
    13: "자아-무의식 해리 유도",
    14: "인지 과부하"
}

def analyze_text(text):
    # Basic tokens
    words = [w for w in text.split() if w.strip()]
    num_words = len(words)
    if num_words == 0:
        return None
        
    # Sentences split by . ? !
    sentences = re.split(r'[.?!]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 0]
    num_sentences = len(sentences)
    if num_sentences == 0:
        return None
        
    # Words per sentence
    wps_list = [len(s.split()) for s in sentences]
    avg_wps = np.mean(wps_list)
    std_wps = np.std(wps_list) if len(wps_list) > 1 else 0.0
    
    # Comma density
    num_commas = text.count(',')
    commas_per_word = num_commas / num_words
    
    # Anchors
    lower_text = text.lower()
    num_and = len(re.findall(r'\band\b', lower_text))
    num_now = len(re.findall(r'\bnow\b', lower_text))
    num_but = len(re.findall(r'\bbut\b', lower_text))
    
    and_ratio = num_and / num_words
    now_ratio = num_now / num_words
    
    return {
        'avg_wps': avg_wps,
        'std_wps': std_wps,
        'commas_per_word': commas_per_word,
        'and_ratio': and_ratio,
        'now_ratio': now_ratio,
        'total_words': num_words
    }

def main():
    print("Loading datasets...")
    df_clusters = pd.read_csv(INPUT_CSV)
    cluster_ids = df_clusters['cluster'].tolist()
    
    metrics = []
    
    with open(INPUT_JSONL, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if not line.strip(): continue
            try:
                record = json.loads(line)
                output_text = record.get('output', '')
                cid = cluster_ids[i]
                
                res = analyze_text(output_text)
                if res is not None:
                    res['cluster_id'] = cid
                    metrics.append(res)
            except Exception as e:
                pass

    df_metrics = pd.DataFrame(metrics)
    
    # Group by cluster and calculate means
    grouped = df_metrics.groupby('cluster_id').mean()
    
    with open(OUTPUT_TXT, 'w', encoding='utf-8') as out:
        out.write("=== ERICKSON RHYTHM & DENSITY ANALYSIS ===\n\n")
        
        # Sort by avg words per sentence (Longest to Shortest breaths)
        sorted_wps = grouped.sort_values('avg_wps', ascending=False)
        out.write("1. 🗣️ AVERAGE WORDS PER SENTENCE (호흡의 길이 - 만연체 vs 간결체)\n")
        out.write("가장 긴 문장(소설형)부터 가장 짧은 문장(가슴을 치는 단타형)까지 순위\n")
        for cid, row in sorted_wps.iterrows():
            out.write(f"- {CLUSTER_NAMES.get(cid)}: {row['avg_wps']:.2f} words/sentence\n")
            
        out.write("\n\n2. 🌊 SENTENCE LENGTH VARIANCE (문장 요동성 - 예측 불허 리듬)\n")
        out.write("문장의 길이가 짧았다 길어졌다 크게 요동치며 멀미(트랜스)를 유도하는 순위\n")
        sorted_std = grouped.sort_values('std_wps', ascending=False)
        for cid, row in sorted_std.iterrows():
            out.write(f"- {CLUSTER_NAMES.get(cid)}: {row['std_wps']:.2f} standard dev.\n")
            
        out.write("\n\n3. ⏱️ COMMA DENSITY (쉼표 밀도 - 의도적인 정지와 침묵)\n")
        out.write("100단어 당 쉼표 사용 횟수 (머뭇거림, 최면적 응시 타임)\n")
        sorted_commas = grouped.sort_values('commas_per_word', ascending=False)
        for cid, row in sorted_commas.iterrows():
            out.write(f"- {CLUSTER_NAMES.get(cid)}: {(row['commas_per_word']*100):.2f} commas per 100 words\n")
            
        out.write("\n\n4. 🔗 THE 'AND' ANCHOR (비판 회피형 연사)\n")
        out.write("100단어 당 'And(그리고)'를 사용하여 논리적 단절 없이 밀어붙이는 순위\n")
        sorted_and = grouped.sort_values('and_ratio', ascending=False)
        for cid, row in sorted_and.iterrows():
            out.write(f"- {CLUSTER_NAMES.get(cid)}: {(row['and_ratio']*100):.2f}%\n")

    print(f"Rhythm analysis complete. Results saved to {OUTPUT_TXT}")

if __name__ == "__main__":
    main()
