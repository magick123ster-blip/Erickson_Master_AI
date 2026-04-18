import pandas as pd
import collections
import re

def extract():
    df = pd.read_csv('erickson_sequences_with_submacros.csv')
    
    all_keywords = []
    for pid in df['pattern_id'].dropna():
        # Split by underscore and ignore 'ERICKSON'
        parts = pid.split('_')
        keywords = [p for p in parts if p and p != 'ERICKSON']
        all_keywords.extend(keywords)
    
    counter = collections.Counter(all_keywords)
    
    # Save to CSV
    result_df = pd.DataFrame(counter.most_common(), columns=['Keyword', 'Frequency'])
    result_df.to_csv('erickson_keyword_inventory.csv', index=False)
    print(f"Total unique keywords: {len(counter)}")
    print(f"Top 20 keywords:\n{result_df.head(20)}")

if __name__ == "__main__":
    extract()
