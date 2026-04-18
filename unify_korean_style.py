import json
import os
import re

DNA_FILE = r'C:\Users\magic\Downloads\erickson_data\erickson_chapter_dna.json'

def unify_korean_style(text):
    if not isinstance(text, str): return text
    
    # Simple replacement mappings for common polite to plain endings
    # This is a heuristic approach, but for these specific texts it should be effective.
    substitutions = [
        (r'있습니다\.', '있다.'),
        (r'합니다\.', '한다.'),
        (r'됩니다\.', '된다.'),
        (r'입니다\.', '이다.'),
        (r'강조합니다\.', '강조한다.'),
        (r'유도합니다\.', '유도한다.'),
        (r'만듭니다\.', '만든다.'),
        (r'구축합니다\.', '구축한다.'),
        (r'제공합니다\.', '제공한다.'),
        (r'활용합니다\.', '활용한다.'),
        (r'의미합니다\.', '의미한다.'),
        (r'제시합니다\.', '제시한다.'),
        (r'수행합니다\.', '수행한다.'),
        (r'자극합니다\.', '자극한다.'),
        (r'구성합니다\.', '구성한다.'),
        (r'위함입니다\.', '위함이다.'),
        (r'기법입니다\.', '기법이다.'),
        (r'원리입니다\.', '원리이다.'),
        (r'것입니다\.', '것이다.'),
        (r'않습니다\.', '않는다.'),
        (r'보여줍니다\.', '보여준다.'),
        (r'해결합니다\.', '해결한다.'),
        (r'수용합니다\.', '수용한다.'),
        (r'형성합니다\.', '형성한다.'),
        (r'독려합니다\.', '독려한다.'),
        (r'사용합니다\.', '사용한다.'),
        (r'정의합니다\.', '정의한다.'),
        (r'암시합니다\.', '암시한다.'),
        (r'메커니즘입니다\.', '메커니즘이다.'),
        (r'전략입니다\.', '전략이다.'),
        (r'기술입니다\.', '기술이다.'),
        (r'의도입니다\.', '의도이다.'),
        (r'나열합니다\.', '나열한다.'),
        (r'강구합니다\.', '강구한다.')
    ]
    
    new_text = text
    for pattern, replacement in substitutions:
        new_text = re.sub(pattern, replacement, new_text)
    
    # Fix some specific multi-line or mid-sentence polite markers if any
    new_text = re.sub(r'임입니다\.', '임이다.', new_text)
    new_text = re.sub(r'감입니다\.', '감이다.', new_text)
    
    return new_text

def execute_unification():
    with open(DNA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for situation in data:
        for entry in data[situation]:
            entry['logic'] = unify_korean_style(entry['logic'])

    with open(DNA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print("Korean style unification complete: erickson_chapter_dna.json")

if __name__ == "__main__":
    execute_unification()
