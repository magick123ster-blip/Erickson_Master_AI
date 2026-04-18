import json
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def load_data(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                item = json.loads(line)
                raw_context = item.get('context_analysis', '')
                raw_reasoning = item.get('reasoning_trace', '')
                
                # Ensure they are strings
                context_str = json.dumps(raw_context) if isinstance(raw_context, dict) else str(raw_context)
                reasoning_str = json.dumps(raw_reasoning) if isinstance(raw_reasoning, dict) else str(raw_reasoning)
                
                data.append({
                    'context': context_str,
                    'reasoning': reasoning_str,
                    'pattern': item.get('pattern_id', 'UNKNOWN'),
                    'output': item.get('output', '')
                })
            except:
                continue
    return pd.DataFrame(data)

def extract_decision_rules(df):
    print("Extracting Decision Rules...")
    # Combine context and reasoning for rules
    df['combined_text'] = df['context'] + " " + df['reasoning']
    
    vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
    X = vectorizer.fit_transform(df['combined_text'])
    y = df['pattern']
    
    # Simple tree to extract interpretable rules
    clf = DecisionTreeClassifier(max_depth=5)
    clf.fit(X, y)
    
    feature_names = vectorizer.get_feature_names_out()
    rules = export_text(clf, feature_names=list(feature_names))
    return rules

def cluster_cognitive_frames(df, n_clusters=12):
    print(f"Clustering into {n_clusters} Cognitive Frames...")
    vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
    X = vectorizer.fit_transform(df['reasoning'])
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df['cluster'] = kmeans.fit_predict(X)
    
    # Get top keywords for each cluster
    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()
    
    cluster_info = {}
    for i in range(n_clusters):
        top_terms = [terms[ind] for ind in order_centroids[i, :7]]
        cluster_info[i] = top_terms
        
    return df, cluster_info

if __name__ == "__main__":
    file_path = r'C:\Users\magic\Downloads\erickson_data\augmented_scripts_full.jsonl'
    df = load_data(file_path)
    
    # 1. Decision Tree Rules
    rules = extract_decision_rules(df)
    with open('decision_rules.txt', 'w', encoding='utf-8') as f:
        f.write(rules)
    print("Decision rules saved to decision_rules.txt")
    
    # 2. Clustering
    df, frames = cluster_cognitive_frames(df)
    
    print("\n## Erickson's Core Cognitive Frames (Clusters)")
    for cid, keywords in frames.items():
        print(f"Frame {cid+1}: {', '.join(keywords)}")
    
    # Summary of patterns per cluster
    print("\n## Patterns per Frame (Sample)")
    for cid in range(len(frames)):
        top_patterns = df[df['cluster'] == cid]['pattern'].value_counts().head(3).index.tolist()
        print(f"Frame {cid+1} typical patterns: {', '.join(top_patterns)}")

    # Dimensionality Reduction for Visualization (Saving data for report)
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(TfidfVectorizer(max_features=500, stop_words='english').fit_transform(df['reasoning']).toarray())
    df['pca1'] = X_pca[:, 0]
    df['pca2'] = X_pca[:, 1]
    df.to_csv('analysis_results.csv', index=False)
    print("Analysis results saved to analysis_results.csv")
