import chromadb
from chromadb.utils import embedding_functions
import re
import os

def integrate_metaphors():
    # 1. Setup ChromaDB
    db_path = 'erickson_vector_db'
    client = chromadb.PersistentClient(path=db_path)
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    collection = client.get_or_create_collection(name="erickson_strategies", embedding_function=emb_fn)

    # 2. Read and Parse Metaphors
    file_path = r'c:\Users\magic\Downloads\erickson_data\metaphors_summary.txt'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by Metaphor markers
    metaphor_blocks = re.split(r'--- Metaphor \d+ ---', content)[1:]
    
    documents = []
    metadatas = []
    ids = []

    for i, block in enumerate(metaphor_blocks):
        output_match = re.search(r'Output:\s*(.*?)\s*Reasoning:', block, re.DOTALL)
        reasoning_match = re.search(r'Reasoning:\s*(.*)', block, re.DOTALL)
        
        if output_match and reasoning_match:
            output_text = output_match.group(1).strip()
            reasoning_text = reasoning_match.group(1).strip()
            
            # Combine for the vector document
            full_text = f"[Erickson Metaphor]\nOutput: {output_text}\n\nReasoning: {reasoning_text}"
            
            documents.append(full_text)
            metadatas.append({
                "type": "metaphor",
                "index": i + 1,
                "history": "Metaphorical Intervention"
            })
            ids.append(f"metaphor_{i+1}")

    # 3. Add to Collection
    if documents:
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Successfully integrated {len(documents)} metaphors into ChromaDB.")
    else:
        print("No metaphors found to integrate.")

if __name__ == "__main__":
    integrate_metaphors()
