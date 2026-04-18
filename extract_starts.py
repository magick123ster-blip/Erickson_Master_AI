import pandas as pd
import os

DATA_DIR = r'C:\Users\magic\Downloads\erickson_data'
INPUT_CSV = os.path.join(DATA_DIR, 'erickson_sequences.csv')

def analyze_openings():
    df = pd.read_csv(INPUT_CSV)
    df = df.sort_values(by=['script_id', 'turn_no'])
    
    macro_starts = []
    micro_starts = []
    first_macro = []
    
    for name, group in df.groupby('script_id'):
        if len(group) >= 3:
            macros = group['pattern_label'].str.upper().tolist()[:3]
            micros = group['pattern_id'].tolist()[:3]
            macro_starts.append(" -> ".join(macros))
            micro_starts.append(" -> ".join(micros))
            first_macro.append(macros[0])
            
    print("=== Most Frequent Starting Techniques (Macro) ===")
    print(pd.Series(first_macro).value_counts().head(5))
            
    print("\n=== Most Frequent 3-Step Opening Chains (Macro) ===")
    print(pd.Series(macro_starts).value_counts().head(5))
    
    print("\n=== Most Frequent 3-Step Opening Chains (Micro) ===")
    print(pd.Series(micro_starts).value_counts().head(5))

    # Output some real examples of these starts
    print("\n=== Example Openings ===")
    for name, group in list(df.groupby('script_id'))[:3]:
        texts = group['content'].tolist()[:3]
        labels = group['pattern_id'].tolist()[:3]
        print(f"Script: {name}")
        for i in range(min(3, len(texts))):
            print(f"[{labels[i]}] {texts[i]}")
        print("-" * 40)

if __name__ == '__main__':
    analyze_openings()
