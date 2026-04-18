import json
import os

def convert_to_vertex_ai(input_file, output_file, system_instruction):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    vertex_records = []
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            try:
                item = json.loads(line)
                
                # Check if it's already in the 'contents' format
                if 'contents' in item:
                    contents = item['contents']
                else:
                    # Map from our standard augmented format
                    user_text = f"지시: {item.get('instruction', '')}\n문맥: {item.get('context_analysis', {}).get('topic', '')}"
                    assistant_text = f"사고 과정: {item.get('reasoning_trace', '')}\n에릭슨 발화: {item.get('output', '')}"
                    
                    contents = [
                        {"role": "user", "parts": [{"text": user_text}]},
                        {"role": "model", "parts": [{"text": assistant_text}]}
                    ]
                
                # Vertex AI SFT JSONL format typically includes systemInstruction per line
                record = {
                    "systemInstruction": {"role": "system", "parts": [{"text": system_instruction}]},
                    "contents": contents
                }
                vertex_records.append(record)
            except:
                continue

    with open(output_file, 'w', encoding='utf-8') as out:
        for rec in vertex_records:
            out.write(json.dumps(rec, ensure_ascii=False) + "\n")
            
    print(f"Successfully converted {len(vertex_records)} records to {output_file}")

if __name__ == "__main__":
    base_dir = r"C:\Users\magic\Downloads\erickson_data"
    
    erickson_system = (
        "당신은 밀턴 에릭슨의 스타일을 완벽하게 재현하는 인공지능입니다. "
        "전략적인 사고 과정(Reasoning Trace)을 먼저 설명하고, 그에 따른 에릭슨의 실제 발화(Output)를 출력하세요."
    )
    
    # Vertex Full
    convert_to_vertex_ai(
        os.path.join(base_dir, "augmented_scripts_full.jsonl"),
        os.path.join(base_dir, "erickson_vertex_full_7937.jsonl"),
        erickson_system
    )
    
    # Vertex Essential
    convert_to_vertex_ai(
        os.path.join(base_dir, "erickson_tuning_essential_1500.jsonl"),
        os.path.join(base_dir, "erickson_vertex_essential_1500.jsonl"),
        erickson_system
    )
