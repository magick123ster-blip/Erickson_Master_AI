import chromadb
from chromadb.utils import embedding_functions
import sys
import os

# Ensure user site-packages are found
sys.path.append(os.path.expanduser("~/AppData/Roaming/Python/Python313/site-packages"))

def query_erickson(user_query, n_results=3):
    db_path = 'erickson_vector_db'
    
    # 1. Connect to Local DB
    client = chromadb.PersistentClient(path=db_path)
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    collection = client.get_collection(name="erickson_strategies", embedding_function=emb_fn)
    
    # 2. Search
    print(f"\n[에릭슨 전략 라이브러리 검색 중: '{user_query}']")
    results = collection.query(
        query_texts=[user_query],
        n_results=n_results
    )
    
    # 3. Display Results
    for i in range(len(results['documents'][0])):
        doc = results['documents'][0][i]
        meta = results['metadatas'][0][i]
        
        print(f"\n--- 유사 사례 #{i+1} ---")
        print(f"▶ 이전 대화 흐름(History): {meta['history']}")
        print(f"▶ 에릭슨의 사고 및 개입 내용:\n{doc}")
        print("-" * 50)

if __name__ == "__main__":
    # Example Query: 저항이 있는 상황에서의 다음 기법과 의도
    # This simulates asking the DB about a specific situation
    test_query = "내담자가 저항을 보일 때 에릭슨이 사용한 전략적 중단과 그 이유"
    query_erickson(test_query)
