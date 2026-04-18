import json

json_path = r"C:\Users\magic\Downloads\erickson_data\algo_bank_results.json"
output_path = r"C:\Users\magic\.gemini\antigravity\brain\20e5a5ff-23f2-4e4b-b6ce-921506df9f91\erickson_algorithm_bank.md"

def generate_bank_report():
    with open(json_path, 'r', encoding='utf-8') as f:
        d = json.load(f)
    
    report = f"""# 에릭슨 알고리즘 뱅크: 7,937개 데이터 기반 핵심 매커니즘
**Ericksonian Algorithm Bank: Core Mechanisms from 7,937 Samples**

이 리포트는 기본 문법 규칙을 넘어, 밀턴 에릭슨이 내담자의 심리 체계를 재설정하기 위해 사용한 **6가지 고위 수준 알고리즘**을 분석한 결과입니다.

---

## 1. 선택의 아키텍처: 이중 구속 (Decision Algorithm: Double Binds)
내담자에게 두 가지 이상의 선택지를 주지만, 어떤 선택을 하더라도 치료적 결과로 귀결되게 설계된 논리 구조입니다.
- **데이터 기반 통계**: 약 **{d['stats']['double_bind']}개**의 샘플에서 발견.
- **핵심 수식**: `[Choice A] OR [Choice B] -> [Single Clinical Outcome]`
- **데이터 증거**:
"""
    for s in d['data']['double_bind'][:3]:
        report += f"- \"{s['t'].strip()}\" (Ref: {s['p']})\n"
    
    report += f"""
---

## 2. 시공간 이동 알고리즘 (Temporal Displacement)
과거의 기억이나 미래의 가능성으로 내담자의 의식을 이동시켜 현재의 고착을 해결합니다.
- **데이터 기반 통계**: 약 **{d['stats']['temporal_displacement']}개**의 샘플에서 발견.
- **핵심 수식**: `[Recall/Imagine] + [Specific Timeframe] -> [Access Resource]`
- **데이터 증거**:
"""
    for s in d['data']['temporal_displacement'][:3]:
        report += f"- \"{s['t'].strip()}\" (Ref: {s['p']})\n"

    report += f"""
---

## 3. 역발상 암시 알고리즘 (Negative Suggestion/Reverse)
"~하지 마라"는 부정을 통해 오히려 그 행동이나 생각을 강화하거나 유도하는 고도의 역설적 기법입니다.
- **데이터 기반 통계**: 약 **{d['stats']['negative_suggestion']}개**의 샘플에서 발견.
- **핵심 수식**: `[Do NOT] + [Positive Goal] -> [Unconscious Attempt]`
- **데이터 증거**:
"""
    for s in d['data']['negative_suggestion'][:3]:
        report += f"- \"{s['t'].strip()}\" (Ref: {s['p']})\n"

    report += f"""
---

## 4. 추상적 의미 압축 (Semantic Compression/Nominalization)
구체적인 대상이 없는 추상 명사를 사용하여 내담자가 자신의 고유한 의미로 그 빈칸을 채우게 만듭니다.
- **데이터 기반 통계**: 약 **{d['stats']['nominalization_ambiguity']}개**의 샘플에서 발견.
- **핵심 수식**: `[Abstract Noun] + [Permissive Verb] -> [Internal Search]`
- **데이터 증거**:
"""
    for s in d['data']['nominalization_ambiguity'][:3]:
        report += f"- \"{s['t'].strip()}\" (Ref: {s['p']})\n"

    report += f"""
---

## 5. 신체-사고 동기화 (Sensorimotor Algorithm: Ideomotor)
사소한 신체 움직임을 특정 심리적 상태나 성취와 강력하게 결합(Linking)합니다.
- **데이터 기반 통계**: 약 **{d['stats']['ideomotor_linking']}개**의 샘플에서 발견.
- **핵심 수식**: `[Involuntary Movement] + [Thought/Knowing] -> [State Anchor]`
- **데이터 증거**:
"""
    for s in d['data']['ideomotor_linking'][:3]:
        report += f"- \"{s['t'].strip()}\" (Ref: {s['p']})\n"

    report += f"""
---

## 6. 중첩된 암시 (Information Interspersal)
평범해 보이는 대화 속에 치료적 핵심 명령을 흩뿌려 의식의 저항을 최소화하고 무의식에 직접 전달합니다.
- **데이터 기반 통계**: 약 **{d['stats']['embedded_commands']}개**의 샘플에서 발견.
- **핵심 수식**: `[Surface Story] + [Embedded Command] -> [Bypass Critical Filter]`
- **데이터 증거**:
"""
    for s in d['data']['embedded_commands'][:3]:
        report += f"- \"{s['t'].strip()}\" (Ref: {s['p']})\n"

    report += """
---

## 📊 알고리즘 뱅크 요약 및 통찰
분석된 **7,937개의 데이터**는 에릭슨의 대화가 즉흥적인 영감이 아니라, 이 6가지 알고리즘 블록의 정교한 조합임을 보여줍니다. 특히 **'시간 이동(Temporal)'**과 **'중첩된 암시(Embedded)'**는 그의 임상 실무에서 가장 높은 비중을 차지하는 핵심 엔진입니다. 이 알고리즘 뱅크는 에릭슨의 사고 체계를 프로그래밍 가능한 수준으로 이해하는 데 결정적인 지표가 됩니다.
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print("Algorithm Bank Report generated successfully.")

if __name__ == "__main__":
    generate_bank_report()
