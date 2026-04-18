import chromadb
from chromadb.utils import embedding_functions
import json
import pandas as pd
from tqdm import tqdm
import os

def build_db():
    dataset_path = 'erickson_deep_learning_dataset.jsonl'
    db_path = 'erickson_vector_db'
    
    # 1. Initialize ChromaDB (Local Persistent)
    print("Initializing Local Vector Database...")
    client = chromadb.PersistentClient(path=db_path)
    
    # 2. Set up Embedding Function (Lightweight & Free)
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    # 3. Create or Get Collection
    collection = client.get_or_create_collection(
        name="erickson_strategies",
        embedding_function=emb_fn,
        metadata={"hnsw:space": "cosine"}
    )
    
    # 4. Load Dataset
    print(f"Loading dataset from {dataset_path}...")
    data = []
    with open(dataset_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
            
    # 5. Indexing in batches
    batch_size = 100
    print(f"Indexing {len(data)} strategies into the database...")
    
    for i in tqdm(range(0, len(data), batch_size)):
        batch = data[i:i+batch_size]
        
        ids = [f"id_{j}" for j in range(i, i + len(batch))]
        documents = [item['output'] for item in batch]
        metadatas = [
            {
                "instruction": item['instruction'],
                "history": item['input'],
                "macro_goal": item['input'].split(':')[-1].strip()
            } for item in batch
        ]
        
        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )
        
    print(f"Successfully built the Erickson Strategy DB at '{db_path}'")
    print(f"Total entries indexed: {collection.count()}")

if __name__ == "__main__":
    build_db()
