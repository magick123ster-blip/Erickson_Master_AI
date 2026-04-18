import pandas as pd
import os

DATA_DIR = r'C:\Users\magic\Downloads\erickson_data'
INPUT_CSV = os.path.join(DATA_DIR, 'erickson_sequences.csv')

def find_pairs():
    df = pd.read_csv(INPUT_CSV)
    df = df.sort_values(by=['script_id', 'turn_no'])
    
    pairs_to_find = [
        ('ERICKSON_CHALLENGE_CONSCIOUSNESS', 'ERICKSON_PATTERN_INTERRUPT'),
        ('ERICKSON_INTERNAL_FOCUS', 'ERICKSON_CONSCIOUS_UNCONSCIOUS_DISSOCIATION'),
        ('ERICKSON_PACING_INTERNAL_STATE', 'ERICKSON_NEGATIVE_SUGGESTION'),
        ('ERICKSON_APPOSITION_OPPOSITES', 'ERICKSON_APPOSITION_OPPOSITES'),
        ('ERICKSON_CONTINGENT_SUGGESTION', 'ERICKSON_CONTINGENT_SUGGESTION')
    ]
    
    with open('real_examples.txt', 'w', encoding='utf-8') as f:
        for name, group in df.groupby('script_id'):
            patterns = group['pattern_id'].tolist()
            contents = group['content'].tolist()
            for i in range(len(patterns)-1):
                pair = (patterns[i], patterns[i+1])
                if pair in pairs_to_find:
                    f.write(f"[{pair[0]} -> {pair[1]}]\n")
                    f.write(f"Script: {name}\n")
                    f.write(f"1: {contents[i]}\n")
                    f.write(f"2: {contents[i+1]}\n")
                    f.write("-" * 40 + "\n")
                    pairs_to_find.remove(pair) # Only find 1 example per pair
                    if not pairs_to_find: return

if __name__ == '__main__':
    find_pairs()
