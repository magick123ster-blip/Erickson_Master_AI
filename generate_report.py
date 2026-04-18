import json

json_path = r"C:\Users\magic\Downloads\erickson_data\rule_evidence_results.json"
output_path = r"C:\Users\magic\.gemini\antigravity\brain\20e5a5ff-23f2-4e4b-b6ce-921506df9f91\generative_grammar_evidence.md"

def generate_report():
    with open(json_path, 'r', encoding='utf-8') as f:
        d = json.load(f)
    
    report = f"""# 에릭슨 생성 문법의 데이터 기반 분석 (Evidence & Data)

본 보고서는 7,937개의 데이터를 전수 조사하여 도출된 '에릭슨 생성 문법(Generative Grammar)'의 실제 근거와 통계적 사례를 제시합니다.

---

## Rule 1: 자아 해리 (Egological Split)
**[문법구조]**: `[의식적 주체] + [무의식적 주체]를 명시적으로 분리하여 대조`
- **통계**: 7,937개 구절 중 약 **{d['stats']['rule1_count']}개**에서 명확한 해리 구조 발견.
- **데이터 증거**:
"""
    for s in d['rule1'][:3]:
        report += f"- \"{s['text'].strip()}\" (Reference: {s['pattern']})\n"
    
    report += f"""
---

## Rule 2: 조건부 유도 (Conditional Leading)
**[문법구조]**: `[As/When + 사실적 행동] -> [Then/Would + 심리적 변화]`
- **통계**: 약 **{d['stats']['rule2_count']}개**의 구절에서 인과 관계를 위장한 암시 구조 발견.
- **데이터 증거**:
"""
    for s in d['rule2'][:3]:
        report += f"- \"{s['text'].strip()}\" (Reference: {s['pattern']})\n"
    
    report += f"""
---

## Rule 3: 허용적 불확실성 (Permissive Uncertainty)
**[문법구조]**: `[I wonder / I don't know]를 활용한 비지시적 제안`
- **통계**: 약 **{d['stats']['rule3_count']}개**의 구절에서 상대방의 선택권을 존중하는 듯한 불확실성 어구 발견.
- **데이터 증거**:
"""
    for s in d['rule3'][:3]:
        report += f"- \"{s['text'].strip()}\" (Reference: {s['pattern']})\n"
    
    report += """
---

## 결론 및 데이터 요약
분석 결과, 에릭슨의 문장은 단순한 말재주가 아니라 **'의식과 무의식의 분리(Rule 1)'**와 **'사실과 암시의 연결(Rule 2)'**이라는 명확한 수식을 따르고 있음이 통계적으로 확인되었습니다. 특히 Rule 2는 가장 빈번하게 사용되는 '리딩(Leading)'의 핵심 문법입니다.
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print("Report generated successfully.")

if __name__ == "__main__":
    generate_report()
