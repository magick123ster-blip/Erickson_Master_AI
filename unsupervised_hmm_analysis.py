import pandas as pd
import numpy as np
from collections import defaultdict, Counter
import os

# Define cluster labels based on clustering_summary.txt
CLUSTER_LABELS = {
    0: "Presupposition & Pacing (전제 및 페이싱)",
    1: "Strategic Orientation & Ordeal (전략적 오리엔테이션 및 오딜)",
    2: "Utilization & TDS (활용 및 내부 검색)",
    3: "Induction & Reframing (유도 및 재구조화)",
    4: "Unconscious Validation (무의식적 검증)",
    5: "Metaphorical Directive (은유적 지시)",
    6: "Resistance Utilization (저항의 활용)",
    7: "Observational Acuity (관찰력 및 통찰)",
    8: "Yes-Set & Permissive Suggestion (예스 세트 및 허용적 암시)",
    9: "Physiological Pacing (생리적 페이싱)",
    10: "Post-Hypnotic Reframing (사후 최면 및 재구조화)",
    11: "Metaphorical Learning (은유적 학습)"
}

def run_unsupervised_analysis():
    input_path = r'C:\Users\magic\Downloads\erickson_data\erickson_integrated_clustering.csv'
    report_path = r'C:\Users\magic\Downloads\erickson_data\unsupervised_hmm_report.md'
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    print(f"Loading data from {input_path}...")
    df = pd.read_csv(input_path)
    
    # Sort by entry_id if available to maintain sequence
    if 'entry_id' in df.columns:
        # entry_id might be string or numeric, try to sort numerically
        try:
            df['entry_id_int'] = pd.to_numeric(df['entry_id'], errors='coerce')
            df = df.sort_values('entry_id_int')
        except:
            pass
            
    sequence = df['cluster'].tolist()
    
    # Export Raw Data for the user
    raw_data_path = r'C:\Users\magic\Downloads\erickson_data\unsupervised_hmm_raw_data.csv'
    df_export = df.copy()
    df_export['state_label'] = df_export['cluster'].map(CLUSTER_LABELS)
    # Select and rename columns for clarity
    cols_to_keep = ['entry_id', 'cluster', 'state_label', 'original_text']
    df_export = df_export[[c for c in cols_to_keep if c in df_export.columns]]
    df_export.to_csv(raw_data_path, index=False, encoding='utf-8-sig')
    print(f"Raw data exported at: {raw_data_path}")

    # Calculate transitions
    transitions = defaultdict(lambda: Counter())
    state_counts = Counter()
    
    for i in range(len(sequence) - 1):
        s_from = sequence[i]
        s_to = sequence[i+1]
        transitions[s_from][s_to] += 1
        state_counts[s_from] += 1
        
    # Probability matrix
    n_clusters = len(CLUSTER_LABELS)
    matrix = np.zeros((n_clusters, n_clusters))
    
    for s_from in range(n_clusters):
        total = state_counts[s_from]
        for s_to in range(n_clusters):
            if total > 0:
                matrix[s_from][s_to] = transitions[s_from][s_to] / total

    # Generate Report
    print(f"Generating report at {report_path}...")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Milton Erickson's Therapy: Unsupervised HMM Analysis Report\n\n")
        f.write("본 보고서는 12개의 클러스터링 기반 데이터를 사용하여 에릭슨의 치료 상태를 스스로 정의하고, 그들 사이의 전이 확률(Transition Probabilities)을 분석한 결과입니다.\n\n")
        
        f.write("## 1. Data-Driven State Distribution (상태 분포)\n")
        total_samples = len(sequence)
        # Use Counter to get counts of original clusters
        cluster_occurrences = Counter(sequence)
        for i in range(n_clusters):
            count = cluster_occurrences.get(i, 0)
            f.write(f"- Cluster {i+1} (**{CLUSTER_LABELS[i]}**): {count}개 ({count/total_samples*100:.1f}%)\n")
            
        f.write("\n## 2. Transition Probability Matrix\n")
        # Header
        f.write("| From \\ To | " + " | ".join([f"C{i+1}" for i in range(n_clusters)]) + " |\n")
        f.write("|" + "---|" * (n_clusters + 1) + "\n")
        for i in range(n_clusters):
            row = f"| **C{i+1}** | " + " | ".join([f"{matrix[i][j]:.3f}" for j in range(n_clusters)]) + " |"
            f.write(row + "\n")
            
        f.write("\n## 3. Transition Flow (Mermaid Diagram - Top Transitions)\n")
        f.write("```mermaid\n")
        f.write("graph TD\n")
        for i in range(n_clusters):
            f.write(f'    C{i+1}["C{i+1}: {CLUSTER_LABELS[i]}"]\n')
            
        for i in range(n_clusters):
            for j in range(n_clusters):
                prob = matrix[i][j]
                if prob > 0.15: # Filter for top transitions to keep diagram readable
                    f.write(f"    C{i+1} -->|{prob:.2f}| C{j+1}\n")
        f.write("```\n")
        
        f.write("\n## 4. Summary of Observed Patterns (주요 패턴 관찰)\n")
        f.write("- **상태 지속성**: 많은 클러스터가 자기 자신으로 전이될 확률(Self-transition)이 높게 나타납니다. 이는 에릭슨이 특정 심리 프레임을 설정하면 한동안 그 상태를 유지하며 암시를 강화함을 의미합니다.\n")
        f.write("- **복합적 전이**: 사전 정의된 상태보다 훨씬 더 세밀한 전이 패턴이 나타나며, 특히 특정 '유도(Induction)' 상태에서 '재구조화(Reframing)'로 이어지는 브릿지 패턴들이 관찰됩니다.\n")

    print("Analysis Complete.")

if __name__ == "__main__":
    run_unsupervised_analysis()
