import sys
import re
import json

def is_mostly_english(text):
    if not text: return False
    # Remove common labels and markdown formatting to identify the core content
    clean_text = re.sub(r'[\*\>\(\)]|에릭슨 발화|지시어|사고 과정|Context', '', text).strip()
    if not clean_text: return False
    # If contains Korean characters, it's not "mostly English" for our translation purposes
    if re.search('[가-힣]', clean_text): return False
    # Must contain at least one English letter
    if not re.search('[a-zA-Z]', clean_text): return False
    return True

def extract_content(file_path, output_json, start_idx=None, end_idx=None):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by Sample header
    samples = content.split('#### Sample ')
    header = samples[0] # Header/intro part
    samples = samples[1:]
    
    if start_idx is not None and end_idx is not None:
        samples_to_process = samples[start_idx:end_idx]
        offset = start_idx
    else:
        samples_to_process = samples
        offset = 0
    
    extracted_data = []
    
    for i, s in enumerate(samples_to_process):
        real_idx = i + offset
        # We need the full sample ID from the header line
        # The line looks like "1 / 96" or similar
        lines = s.split('\n')
        sample_id_line = lines[0].strip()
        
        sample_fields = {}
        
        current_field = None
        current_text = []

        for line in lines[1:]:
            if line.strip().startswith('> **Output'):
                current_field = 'output'
                current_text = [line]
            elif line.strip().startswith('- **Instruction'):
                if current_field: sample_fields[current_field] = '\n'.join(current_text)
                current_field = 'instruction'
                current_text = [line]
            elif line.strip().startswith('- **Reasoning Trace'):
                if current_field: sample_fields[current_field] = '\n'.join(current_text)
                current_field = 'reasoning'
                current_text = [line]
            elif line.strip().startswith('- **Context:'):
                if current_field: sample_fields[current_field] = '\n'.join(current_text)
                current_field = 'context'
                current_text = [line]
            elif current_field:
                current_text.append(line)
        
        if current_field: sample_fields[current_field] = '\n'.join(current_text)
        
        needs_translation = {}
        for field, text in sample_fields.items():
            if ':' in text:
                content_part = text.split(':', 1)[1]
            else:
                content_part = text
            
            if is_mostly_english(content_part):
                needs_translation[field] = text
        
        if needs_translation:
            extracted_data.append({
                'index': real_idx,
                'header_line': sample_id_line,
                'fields': needs_translation
            })
            
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(extracted_data, f, ensure_ascii=False, indent=2)

    print(f'Extracted {len(extracted_data)} samples requiring translation (Indices {offset} to {offset + len(samples_to_process) - 1}).')

if __name__ == '__main__':
    if len(sys.argv) == 4:
        extract_content('erickson_pattern_bank_v2_complete.md', sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    else:
        extract_content('erickson_pattern_bank_v2_complete.md', 'english_parts.json')
