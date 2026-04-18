import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
import os
import json

def master_integration():
    db_path = 'erickson_vector_db'
    client = chromadb.PersistentClient(path=db_path)
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    collection = client.get_or_create_collection(name="erickson_strategies", embedding_function=emb_fn)

    base_path = 'c:/Users/magic/Downloads/erickson_data'
    
    # 1. Integrate 1,805 Strategic Chains
    chains_file = os.path.join(base_path, 'erickson_all_strategic_chains.csv')
    if os.path.exists(chains_file):
        df = pd.read_csv(chains_file)
        print(f"Integrating {len(df)} strategic chains...")
        
        documents = []
        metadatas = []
        ids = []
        
        for idx, row in df.iterrows():
            content = f"Strategic Chain (Length {row['length']}): {row['chain_sequence']}\n"
            # Add step details if available
            for i in range(1, 11):
                step_id = row.get(f'step_{i}_id')
                step_text = row.get(f'step_{i}_text')
                if pd.notna(step_id) and pd.notna(step_text):
                    content += f"Step {i} [{step_id}]: {step_text}\n"
            
            documents.append(content)
            metadatas.append({"type": "strategic_chain", "length": int(row['length']), "source": "all_strategic_chains.csv"})
            ids.append(f"chain_{idx}")
        
        # Batch add
        for i in range(0, len(documents), 100):
            batch_end = min(i + 100, len(documents))
            collection.add(
                documents=documents[i:batch_end],
                metadatas=metadatas[i:batch_end],
                ids=ids[i:batch_end]
            )
        print("Strategic chains integration complete.")

    # 2. Integrate Summary Text Files (High-level insights)
    summary_files = [
        'clustering_summary.txt', 
        'context_response_summary.txt', 
        'multilayer_summary.txt', 
        'pivots_summary.txt'
    ]
    
    for file_name in summary_files:
        file_path = os.path.join(base_path, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Split by logical sections (simple split by double newline)
                sections = [s.strip() for s in content.split('\n\n') if len(s.strip()) > 50]
                print(f"Integrating {len(sections)} sections from {file_name}...")
                
                for s_idx, section in enumerate(sections):
                    collection.add(
                        documents=[section],
                        metadatas=[{"type": "summary_insight", "source": file_name}],
                        ids=[f"summary_{file_name}_{s_idx}"]
                    )

    print("Master Integration Complete! All strategic brains are fused.")

if __name__ == "__main__":
    master_integration()
