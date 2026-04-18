import json
import os

def convert_to_openai(input_file, output_file, system_prompt):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    openai_records = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                # Assuming the input is in our custom augmented JSON format
                # or the Gemini Chat JSONL format.
                # Let's handle our standard augmented item structure first.
                item = json.loads(line)
                
                # Check if it's the 'contents' format (Gemini Chat)
                if 'contents' in item:
                    user_text = item['contents'][0]['parts'][0]['text']
                    assistant_text = item['contents'][1]['parts'][0]['text']
                else:
                    # Original augmented format
                    user_text = f"지시: {item.get('instruction', '')}\n문맥: {item.get('context_analysis', {}).get('topic', '')}"
                    assistant_text = f"사고 과정: {item.get('reasoning_trace', '')}\n에릭슨 발화: {item.get('output', '')}"
                
                openai_record = {
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_text},
                        {"role": "assistant", "content": assistant_text}
                    ]
                }
                openai_records.append(openai_record)
            except Exception as e:
                print(f"Skipping line due to error: {e}")
                continue

    with open(output_file, 'w', encoding='utf-8') as out:
        for rec in openai_records:
            out.write(json.dumps(rec, ensure_ascii=False) + "\n")
            
    print(f"Successfully converted {len(openai_records)} records to {output_file}")

if __name__ == "__main__":
    base_dir = r"C:\Users\magic\Downloads\erickson_data"
    
    # Master System Prompt for Erickson
    erickson_system_prompt = (
        "당신은 전설적인 최면 치료사 밀턴 에릭슨(Milton Erickson)의 언어 모델입니다. "
        "주어진 지시와 문맥에 따라, 먼저 당신의 전략적인 사고 과정(Reasoning Trace)을 설명한 뒤, "
        "에릭슨 특유의 모호함, 활용(Utilization), 재구성(Reframing), 이중 구속(Double Bind) 등이 담긴 발화를 출력하십시오."
    )
    
    # Convert Essential 1500 (Note: We need the original augmented data or we parse the existing jsonl)
    # The 'erickson_tuning_essential_1500.jsonl' I created was in Gemini format.
    convert_to_openai(
        os.path.join(base_dir, "erickson_tuning_essential_1500.jsonl"),
        os.path.join(base_dir, "erickson_openai_essential_1500.jsonl"),
        erickson_system_prompt
    )
    
    # Convert Full 7937
    convert_to_openai(
        os.path.join(base_dir, "augmented_scripts_full.jsonl"),
        os.path.join(base_dir, "erickson_openai_full_7937.jsonl"),
        erickson_system_prompt
    )
