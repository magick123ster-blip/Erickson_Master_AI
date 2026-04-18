import os

def split_jsonl(input_file, output_prefix, lines_per_file):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        file_count = 1
        line_count = 0
        out_f = None
        
        for line in f:
            if line_count % lines_per_file == 0:
                if out_f:
                    out_f.close()
                output_file = f"{output_prefix}_part{file_count}.txt"
                out_f = open(output_file, 'w', encoding='utf-8')
                print(f"Creating {output_file}...")
                file_count += 1
            
            out_f.write(line)
            line_count += 1
        
        if out_f:
            out_f.close()
    
    print(f"Successfully split into {file_count - 1} files.")

if __name__ == "__main__":
    input_path = r"c:\Users\magic\Downloads\erickson_data\augmented_scripts_full.jsonl.txt"
    output_base = r"c:\Users\magic\Downloads\erickson_data\augmented_scripts_full_jsonl"
    # 7938 lines total, 10 parts -> ~794 lines per part
    split_jsonl(input_path, output_base, 800)
