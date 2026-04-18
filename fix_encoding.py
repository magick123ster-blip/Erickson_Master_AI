import sys

path = r'C:\Users\magic\Downloads\erickson_data\erickson_pattern_bank_v1_translated.md'

try:
    # Try reading as UTF-16 (often what PowerShell writes)
    with open(path, 'rb') as f:
        data = f.read()
    
    # Try common encodings
    content = None
    for enc in ['utf-16', 'utf-8-sig', 'utf-8', 'cp949']:
        try:
            content = data.decode(enc)
            print(f"Successfully decoded with {enc}")
            break
        except:
            continue
            
    if content:
        # Write back as clean UTF-8
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Successfully wrote back as UTF-8")
        
        # Print the last 500 characters to verify
        print("\nLast 500 characters:")
        print(content[-500:])
    else:
        print("Failed to decode file with any common encoding.")

except Exception as e:
    print(f"Error: {e}")
