import os

def split_file_by_chars(input_path, output_dir, chars_per_file=600000):
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    os.makedirs(output_dir, exist_ok=True)
    
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    total_chars = len(content)
    num_files = (total_chars // chars_per_file) + (1 if total_chars % chars_per_file != 0 else 0)
    
    print(f"Total characters: {total_chars}")
    print(f"Target characters per file: {chars_per_file}")
    print(f"Number of files to create: {num_files}")
    
    for i in range(num_files):
        start = i * chars_per_file
        end = min((i + 1) * chars_per_file, total_chars)
        
        # Try to find the next newline to avoid splitting in the middle of a line
        if end < total_chars:
            next_newline = content.find('\n', end)
            if next_newline != -1 and next_newline < end + 5000: # Small buffer
                end = next_newline + 1
        
        chunk = content[start:end]
        output_path = os.path.join(output_dir, f"erickson_pattern_bank_v1_part{i+1}.txt")
        
        with open(output_path, 'w', encoding='utf-8') as out_f:
            out_f.write(chunk)
            
        print(f"Created: {os.path.basename(output_path)} ({len(chunk)} chars)")

if __name__ == "__main__":
    input_file = r"C:\Users\magic\.gemini\antigravity\brain\c3467b02-37b1-45e1-8ba3-ea06a487e8ce\erickson_pattern_bank_v1.md"
    output_folder = r"C:\Users\magic\Downloads\erickson_data\split_bank"
    
    # 600,000 characters is roughly 200,000 tokens for mixed text
    split_file_by_chars(input_file, output_folder, 600000)
