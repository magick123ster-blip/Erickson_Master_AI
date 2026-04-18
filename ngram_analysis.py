import json
from collections import Counter
import nltk
from nltk.util import ngrams
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder

# Ensure nltk resources (though we use spaCy normally, nltk is great for collocations)
# nltk.download('punkt')

def load_data(file_path):
    print(f"Loading data from {file_path}...")
    outputs = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                item = json.loads(line)
                outputs.append(item.get('output', '').lower())
            except:
                continue
    return outputs

def analyze_ngrams_and_collocations(texts):
    print("Analyzing N-grams and Collocations...")
    all_words = []
    for text in texts:
        # Simple tokenization for N-grams
        tokens = [t for t in text.replace('.', ' . ').replace(',', ' , ').split() if t.isalnum()]
        all_words.extend(tokens)
    
    # 1. N-grams (2, 3, 4)
    bigrams = Counter(ngrams(all_words, 2))
    trigrams = Counter(ngrams(all_words, 3))
    quadgrams = Counter(ngrams(all_words, 4))
    
    # 2. Collocations (Bigrams with high Pointwise Mutual Information)
    finder = BigramCollocationFinder.from_words(all_words)
    finder.apply_freq_filter(5) # At least 5 occurrences
    measures = BigramAssocMeasures()
    top_collocations = finder.nbest(measures.pmi, 20)
    
    return bigrams, trigrams, quadgrams, top_collocations

if __name__ == "__main__":
    file_path = r'C:\Users\magic\Downloads\erickson_data\augmented_scripts_full.jsonl'
    texts = load_data(file_path)
    
    b, t, q, colls = analyze_ngrams_and_collocations(texts)
    
    print("\n## N-gram Analysis Results")
    
    print("\n### Top 10 Bigrams")
    for gram, count in b.most_common(10):
        print(f"- {' '.join(gram)}: {count}")
        
    print("\n### Top 10 Trigrams")
    for gram, count in t.most_common(10):
        print(f"- {' '.join(gram)}: {count}")
        
    print("\n### Top 10 Quadgrams")
    for gram, count in q.most_common(10):
        print(f"- {' '.join(gram)}: {count}")

    print("\n### Top 20 Collocations (PMI)")
    for gram in colls:
        print(f"- {' '.join(gram)}")

    # Save summary for report
    summary = {
        "bigrams": [" ".join(g) for g, c in b.most_common(50)],
        "trigrams": [" ".join(g) for g, c in t.most_common(50)],
        "quadgrams": [" ".join(g) for g, c in q.most_common(50)],
        "collocations": [" ".join(g) for g in colls]
    }
    with open('ngram_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
