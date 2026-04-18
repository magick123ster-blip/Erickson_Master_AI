import json
import pandas as pd

def generate_ngram_csv(json_summary, output_csv):
    print(f"Generating N-gram raw data CSV from {json_summary}...")
    
    with open(json_summary, 'r', encoding='utf-8') as f:
        summary = json.load(f)
    
    # We'll create a "long" format for better usability
    # Type, Phrase, Score/Rank
    data = []
    
    # Using most_common was done in the previous script, but summary only has strings
    # We should probably re-run analysis to get counts or just list the top ones from summary
    # Let's re-run a simplified version to get counts for all ngrams if possible
    # but for now, let's transform the summary into a readable table.
    
    for category in ['bigrams', 'trigrams', 'quadgrams', 'collocations']:
        for i, phrase in enumerate(summary[category]):
            data.append({
                'category': category,
                'phrase': phrase,
                'rank': i + 1
            })
            
    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"N-gram raw data saved to {output_csv}")

if __name__ == "__main__":
    generate_ngram_csv('ngram_summary.json', 'erickson_ngram_analysis_raw.csv')
