import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from tqdm import tqdm

def load_data(file_path):
    print(f"Loading data from {file_path}...")
    outputs = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                item = json.loads(line)
                outputs.append(item.get('output', ''))
            except:
                continue
    return outputs

def perform_topic_modeling(texts, n_topics=10):
    print(f"Performing Topic Modeling (LDA) on {len(texts)} entries...")
    
    # Preprocessing using CountVectorizer (LDA works better with counts)
    vectorizer = CountVectorizer(stop_words='english', max_features=2000)
    data_vectorized = vectorizer.fit_transform(texts)
    
    # LDA Model
    lda_model = LatentDirichletAllocation(n_components=n_topics, max_iter=10, learning_method='online', random_state=42)
    lda_output = lda_model.fit_transform(data_vectorized)
    
    # Get keywords for each topic
    feature_names = vectorizer.get_feature_names_out()
    topics_data = []
    for topic_idx, topic in enumerate(lda_model.components_):
        top_keywords = [feature_names[i] for i in topic.argsort()[:-11:-1]]
        topics_data.append({
            "topic_id": topic_idx,
            "keywords": ", ".join(top_keywords)
        })
        
    # Assign dominant topic to each text
    df_results = pd.DataFrame(lda_output)
    dominant_topics = df_results.idxmax(axis=1)
    
    raw_results = []
    for i, text in enumerate(texts):
        raw_results.append({
            "text": text,
            "dominant_topic": dominant_topics[i],
            "topic_contribution": df_results.iloc[i, dominant_topics[i]]
        })
        
    return pd.DataFrame(topics_data), pd.DataFrame(raw_results)

if __name__ == "__main__":
    file_path = r'C:\Users\magic\Downloads\erickson_data\augmented_scripts_full.jsonl'
    texts = load_data(file_path)
    
    if texts:
        topics_summary, raw_data = perform_topic_modeling(texts)
        
        print("\n## Topic Modeling Summary")
        print(topics_summary)
        
        # Save results
        topics_summary.to_csv('erickson_topic_keywords.csv', index=False, encoding='utf-8-sig')
        raw_data.to_csv('erickson_topic_analysis_raw.csv', index=False, encoding='utf-8-sig')
        print("\nTopic modeling results saved to CSV files.")
    else:
        print("No data loaded.")
