import tiktoken
import os

input_file = r"c:\Users\magic\Downloads\erickson_data\augmented_scripts_full.txt"
output_dir = r"c:\Users\magic\Downloads\erickson_data"

def split_file(file_path, chunk_size=800000):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(text)
    
    total_tokens = len(tokens)
    print(f"Total tokens: {total_tokens}")
    
    for i in range(0, total_tokens, chunk_size):
        chunk_tokens = tokens[i:i+chunk_size]
        chunk_text = enc.decode(chunk_tokens)
        
        part_num = (i // chunk_size) + 1
        output_file = os.path.join(output_dir, f"augmented_scripts_full_part{part_num}.txt")
        
        with open(output_file, 'w', encoding='utf-8') as out_f:
            out_f.write(chunk_text)
            
        print(f"Saved {output_file} with {len(chunk_tokens)} tokens.")

if __name__ == "__main__":
    split_file(input_file)
