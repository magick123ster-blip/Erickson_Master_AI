import pandas as pd
import spacy
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from tqdm import tqdm
import os
import sys

# Load spaCy
try:
    nlp = spacy.load("en_core_web_sm")
except:
    print("spaCy model 'en_core_web_sm' not found. Please install it.")
    sys.exit(1)

def extract_fsm_patterns(doc):
    """Extract syntactic dependency patterns similar to fsm_analysis_raw."""
    patterns = []
    for token in doc:
        # Simple patterns: Tag(Dep:Tag)
        if token.dep_ != "ROOT":
             patterns.append(f"{token.head.pos_}({token.dep_}:{token.pos_})")
        
        # Longer paths: Verb -> prep -> ADP -> pobj -> NOUN
        if token.pos_ == "VERB":
            for child in token.children:
                if child.dep_ == "prep":
                    for grandchild in child.children:
                        if grandchild.dep_ == "pobj":
                            patterns.append(f"VERB--prep-->ADP--pobj-->{grandchild.pos_}")
                            
        # Others like: ADP--pobj-->NOUN--det-->DET
        if token.pos_ == "ADP" and token.dep_ == "prep":
            for child in token.children:
                if child.dep_ == "pobj":
                    for grandchild in child.children:
                        if grandchild.dep_ == "det":
                            patterns.append(f"ADP--pobj-->{child.pos_}--det-->{grandchild.pos_}")
    return " ".join(patterns)

def run_step1():
    srl_path = r'C:\Users\magic\Downloads\erickson_data\srl_analysis_raw - 복사본.csv'
    jsonl_path = r'C:\Users\magic\Downloads\erickson_data\augmented_scripts_full.jsonl'
    output_path = r'C:\Users\magic\Downloads\erickson_data\erickson_integrated_clustering.csv'

    print("Loading SRL data...")
    try:
        srl_df = pd.read_csv(srl_path, encoding='utf-8-sig')
    except:
        srl_df = pd.read_csv(srl_path, encoding='cp949')
    
    print(f"Loaded {len(srl_df)} SRL entries.")

    # Load JSONL metadata into a dictionary for fast lookup
    metadata = {}
    print("Loading JSONL metadata...")
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                item = json.loads(line)
                # Use output as key, but clean it to avoid minor mismatches
                text_key = item.get('output', '').strip()
                metadata[text_key] = item
            except:
                continue

    print("Integrating data and extracting features...")
    integrated_data = []
    
    # Process all rows in SRL
    for _, row in tqdm(srl_df.iterrows(), total=len(srl_df)):
        text = str(row['original_text'])
        text_key = text.strip()
        meta = metadata.get(text_key, {})
        
        # NLP analysis
        doc = nlp(text)
        fsm = extract_fsm_patterns(doc)
        pos = " ".join([t.pos_ for t in doc])
        
        reasoning = str(meta.get('reasoning_trace', ''))
        # If reasoning is empty in JSONL, maybe it's in a different field or we just keep it empty
        
        entry = {
            'entry_id': row.get('entry_id', 'N/A'),
            'original_text': text,
            'predicate': row.get('predicate', ''),
            'agent': row.get('agent', ''),
            'patient': row.get('patient', ''),
            'manner': row.get('manner', ''),
            'location': row.get('location', ''),
            'pattern_id': meta.get('pattern_id', 'UNKNOWN'),
            'reasoning': reasoning,
            'fsm_patterns': fsm,
            'pos_sequence': pos,
            # Combine text, reasoning, fsm, and pos for clustering
            'combined_features': f"{text} {reasoning} {fsm} {pos}"
        }
        integrated_data.append(entry)

    df_integrated = pd.DataFrame(integrated_data)

    print("Performing Clustering (K-Means)...")
    # We use TF-IDF on the combined features
    vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
    X = vectorizer.fit_transform(df_integrated['combined_features'])
    
    n_clusters = 12
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df_integrated['cluster'] = kmeans.fit_predict(X)
    
    print("Performing Dimensionality Reduction (PCA)...")
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X.toarray())
    df_integrated['pca1'] = X_pca[:, 0]
    df_integrated['pca2'] = X_pca[:, 1]

    print(f"Saving integrated data to {output_path}...")
    df_integrated.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    # Generate Cluster Summary
    print("\n## Cognitive Frame Analysis (K-Means Clusters)")
    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()
    
    cluster_summary = []
    for i in range(n_clusters):
        top_terms = [terms[ind] for ind in order_centroids[i, :7]]
        pattern_dist = df_integrated[df_integrated['cluster'] == i]['pattern_id'].value_counts().head(3).index.tolist()
        summary = f"Cluster {i+1}: Keywords: {', '.join(top_terms)} | Typical Patterns: {', '.join(pattern_dist)}"
        print(summary)
        cluster_summary.append(summary)
        
    # Save a small text report
    with open('clustering_summary.txt', 'w', encoding='utf-8') as f:
        f.write("\n".join(cluster_summary))

if __name__ == "__main__":
    run_step1()
