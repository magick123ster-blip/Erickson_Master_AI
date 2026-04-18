import pandas as pd
import numpy as np
from collections import Counter
import warnings

warnings.filterwarnings('ignore')

INPUT_CSV = r"C:\Users\magic\Downloads\erickson_data\erickson_strategy_clusters.csv"
OUTPUT_TXT = r"C:\Users\magic\Downloads\erickson_data\macro_topology_results.txt"

# This mapping uses the names we established in the Algorithm Map
CLUSTER_NAMES = {
    0: "결핍의 치명적 자산화 (Cluster 1)",
    1: "시간적 지연과 과정의 유예 (Cluster 2)",
    2: "부정적 예스-세트 (Cluster 3)",
    3: "문제의 기술적 해체 (Cluster 4)",
    4: "우회적 성취 루프 (Cluster 5)",
    5: "저항의 역설적 과제화 (Cluster 6)",
    6: "기억 단절을 위한 일상적 닻 (Cluster 7)",
    7: "데이터 기반의 논리 폭파 (Cluster 8)",
    8: "허용적 전제 질문법 (Cluster 9)",
    9: "학술/역사적 닻 내리기 (Cluster 10)",
    10: "최소 개입 페이싱 (Cluster 11)",
    11: "증상 소유권 부여 (Cluster 12)",
    12: "일상 감각의 메타포화 (Cluster 13)",
    13: "자아-무의식 해리 유도 (Cluster 14)",
    14: "인지 과부하 (Cluster 15)"
}

def get_name(cid):
    return CLUSTER_NAMES.get(cid, f"Cluster {cid}")

def main():
    print("Loading data...")
    df = pd.read_csv(INPUT_CSV)
    clusters = df['cluster'].tolist()

    print(f"Total entries: {len(clusters)}")
    
    # Remove consecutive duplicates to focus on true SHIFTS in strategy
    condensed_sequence = []
    for c in clusters:
        if not condensed_sequence or condensed_sequence[-1] != c:
            condensed_sequence.append(c)
            
    print(f"Condensed sequence length (ignoring self-transitions): {len(condensed_sequence)}")
    
    # 1. Calculate Bigrams (A -> B transitions)
    bigrams = []
    for i in range(len(condensed_sequence) - 1):
        bigrams.append((condensed_sequence[i], condensed_sequence[i+1]))
        
    bigram_counts = Counter(bigrams)
    
    # 2. Calculate Trigrams (A -> B -> C transitions) for "Combos"
    trigrams = []
    for i in range(len(condensed_sequence) - 2):
        trigrams.append((condensed_sequence[i], condensed_sequence[i+1], condensed_sequence[i+2]))
        
    trigram_counts = Counter(trigrams)

    with open(OUTPUT_TXT, 'w', encoding='utf-8') as f:
        f.write("=== MACRO-TOPOLOGY: ERICKSON'S MOST FREQUENT STRATEGY SHIFTS ===\n\n")
        
        f.write("--- TOP 10 STRATEGY BIGRAMS (2-Step Combos) ---\n")
        for (a, b), count in bigram_counts.most_common(10):
            f.write(f"[{get_name(a)}] ---> [{get_name(b)}] (빈도: {count})\n")
            
        f.write("\n\n--- TOP 10 STRATEGY TRIGRAMS (3-Step Combos) ---\n")
        for (a, b, c), count in trigram_counts.most_common(10):
            f.write(f"[{get_name(a)}] ---> [{get_name(b)}] ---> [{get_name(c)}] (빈도: {count})\n")

    print(f"Topology analysis complete. Results saved to {OUTPUT_TXT}")

if __name__ == "__main__":
    main()
