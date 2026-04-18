import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

INPUT_JSONL = r"C:\Users\magic\Downloads\erickson_data\augmented_scripts_full.jsonl.txt"
INPUT_CSV = r"C:\Users\magic\Downloads\erickson_data\erickson_strategy_clusters.csv"
OUTPUT_TXT = r"C:\Users\magic\Downloads\erickson_data\context_response_summary.txt"

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

def get_name(cid):
    return CLUSTER_NAMES.get(cid, f"Cluster {cid}")

def main():
    print("Loading datasets...")
    # Load cluster assignments
    df_clusters = pd.read_csv(INPUT_CSV)
    cluster_ids = df_clusters['cluster'].tolist()
    
    # Load JSONL to extract contexts
    contexts = []
    with open(INPUT_JSONL, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip(): continue
            try:
                record = json.loads(line)
                cx = record.get('context_analysis', {})
                topic = cx.get('topic', '')
                tone = cx.get('tone_constraint', '')
                structure = cx.get('structural_constraint', '')
                
                # Combine all context metadata into one document per utterance
                combined = f"{topic} {tone} {structure}"
                contexts.append(combined)
            except Exception as e:
                pass

    if len(contexts) != len(cluster_ids):
        print(f"Mismatch: Contexts({len(contexts)}) vs Clusters({len(cluster_ids)})")
        return

    # Group contexts by cluster
    # 15 distinct documents (one huge string per cluster)
    cluster_docs = {i: "" for i in range(15)}
    for cx, cid in zip(contexts, cluster_ids):
        cluster_docs[cid] += (" " + cx)
        
    doc_list = [cluster_docs[i] for i in range(15)]
    
    # Apply TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english', max_df=0.9)
    X = vectorizer.fit_transform(doc_list)
    feature_names = vectorizer.get_feature_names_out()
    
    # Save the top keywords for each cluster
    with open(OUTPUT_TXT, 'w', encoding='utf-8') as out:
        out.write("=== CONTEXT-RESPONSE MAPPING (TF-IDF TRIGGER WORDS) ===\n\n")
        
        for i in range(15):
            out.write(f"--- [Strategy Cluster {i}: {get_name(i)}] ---\n")
            
            # Get tf-idf scores for this cluster
            row = X.getrow(i).toarray()[0]
            # Get top indices
            # argsort returns lowest to highest, so we take the end and reverse
            top_indices = row.argsort()[-20:][::-1]
            
            top_terms = []
            for idx in top_indices:
                score = row[idx]
                word = feature_names[idx]
                if score > 0.05:  # meaningful threshold
                    top_terms.append(f"{word}({score:.2f})")
                    
            out.write("CONTEXT TRIGGERS (What problems/states trigger this strategy?):\n")
            out.write(", ".join(top_terms) + "\n\n")

    print(f"TF-IDF mapping complete. Results saved to {OUTPUT_TXT}")

if __name__ == "__main__":
    main()
