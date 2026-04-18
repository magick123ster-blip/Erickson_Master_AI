import json
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from collections import Counter
import re
import warnings

warnings.filterwarnings('ignore')

INPUT_FILE = r"C:\Users\magic\Downloads\erickson_data\augmented_scripts_full.jsonl.txt"
OUTPUT_CSV = r"C:\Users\magic\Downloads\erickson_data\erickson_strategy_clusters.csv"
OUTPUT_REPORT = r"C:\Users\magic\.gemini\antigravity\brain\abf69032-42a7-457c-b004-217a131147e3\strategy_discovery_report.md"

def load_data(filepath):
    print(f"Loading data from {filepath}...")
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return pd.DataFrame(data)

def extract_keywords(texts, top_n=5):
    # Very basic keyword extraction based on frequency of words (excluding common stop words)
    stop_words = set(['이', '그', '저', '수', '것', '있는', '있도록', '하는', '한다', '위해', '대한', '통해', '내담자가', '내담자의', '의도한다', '유도한다', '만든다', '사용하여', '한다.', '다.', '있다.'])
    words = []
    for text in texts:
        # Extract korean words loosely
        tokens = re.findall(r'[가-힣]+', text)
        words.extend([t for t in tokens if t not in stop_words and len(t) > 1])
    
    counter = Counter(words)
    return [word for word, count in counter.most_common(top_n)]

def main():
    df = load_data(INPUT_FILE)
    if 'reasoning_trace' not in df.columns or 'output' not in df.columns:
        print("Required columns not found in the dataset.")
        return

    # We want to discover the underlying strategies, so we embed the reasoning_trace
    print(f"Data shape: {df.shape}")
    print("Preparing embedding model (this may take a moment to download the first time)...")
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    print("Encoding texts...")
    embeddings = model.encode(df['reasoning_trace'].tolist(), show_progress_bar=True)

    K = 15
    print(f"Running K-Means clustering with K={K}...")
    kmeans = KMeans(n_clusters=K, random_state=42, n_init='auto')
    df['cluster'] = kmeans.fit_predict(embeddings)

    print(f"Saving fully clustered data to {OUTPUT_CSV}...")
    df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8-sig')

    print("Generating discovery report...")
    report_content = [
        "# 에릭슨 고유 전략의 데이터 주도적 발견 (비지도 군집화 결과)\n",
        "총 7,937개의 에릭슨 발화 데이터를 분석하여, 기존의 분석 틀을 배제하고 인공지능이 스스로 군집화하여 도출해낸 **15개의 오리지널 전략 패턴**입니다.\n",
        "순수하게 에릭슨의 '사고 과정(Reasoning)' 텍스트가 가진 내적 유사도로만 묶였으므로, 각 군집은 **비슷한 심리적 의도와 작동 원리**를 공유합니다.\n\n"
    ]

    for cluster_id in range(K):
        cluster_data = df[df['cluster'] == cluster_id]
        size = len(cluster_data)
        
        # Extract keywords to help label
        keywords = extract_keywords(cluster_data['reasoning_trace'].tolist(), top_n=7)
        
        # We need to create an emergent title based on the data. For now, we list the keywords.
        report_content.append(f"## Cluster {cluster_id + 1}: [전략 키워드: {', '.join(keywords)}]")
        report_content.append(f"- **데이터 수:** {size} 개 ({size/len(df)*100:.1f}%)")
        report_content.append("- **대표 발화 및 사고 과정:**\n")
        
        # Pick 3 representative samples closest to the centroid (for simplicity here, we just take the first 3 or random 3)
        # To be better, we could find the ones closest to the center, but let's just sample for the report
        sample_data = cluster_data.sample(n=min(3, size), random_state=42)
        
        for idx, row in sample_data.iterrows():
            report_content.append(f"  > **Output (발화):** \"{row['output']}\"")
            report_content.append(f"  > **Reasoning (의도):** {row['reasoning_trace']}\n")
        
        report_content.append("---\n")

    with open(OUTPUT_REPORT, 'w', encoding='utf-8') as f:
        f.writelines(report_content)

    print(f"Report saved to Artifacts: {OUTPUT_REPORT}")
    print("Discovery complete!")

if __name__ == "__main__":
    main()
