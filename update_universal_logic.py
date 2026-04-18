import json
import os

DNA_FILE = r'C:\Users\magic\Downloads\erickson_data\erickson_chapter_dna.json'

UNIVERSAL_LOGIC = {
    "ERICKSON_ANTI_PATTERN_CONTRADICTION": "환자의 주관적 고통이나 현실을 직접적으로 부정하는 기존의 의료적 접근(안티 패턴)을 비판하고, 대신 환자의 현실을 인정하는 것이 라포 형성의 핵심임을 강조하는 원리이다.",
    "ERICKSON_CHALLENGE_AUTHORITY": "치료자의 권위에 대한 맹목적인 순응을 경계하고, 내담자가 자신의 행동과 믿음에 대한 내부적 근거를 스스로 찾도록 유도하여 자발적인 변화를 촉진하는 기법이다.",
    "ERICKSON_CHALLENGE_TO_CONSCIOUS_DEFINITION": "내담자가 트랜스 현상을 의식적으로 정의하거나 분석하려 할 때, 불가능한 수준의 정밀한 정의를 요구함으로써 의식의 과부하와 혼란을 유도하고 무의식적 수용성을 높이는 기법이다.",
    "ERICKSON_CONFUSION_BY_PANTOMIME": "언어적 소통이 제한된 상황에서 비언어적 암시를 통해 내담자의 이해 욕구를 자극하고, 이 과정에서 발생하는 정신적 불확실성을 활용하여 암시의 수용성을 극대화하는 기법이다.",
    "ERICKSON_CONSCIOUS_UNCONSCIOUS_DISSOCIATION": "의식과 무의식의 기능을 이분법적으로 분리하여, 의식이 분석이나 방어에 몰두하는 동안 무의식이 치료적 학습을 독립적으로 수행하도록 만드는 핵심 해리 기법이다.",
    "ERICKSON_DISSOCIATION_AFFECT_SPLIT": "지적 이해와 정서적 경험을 분리하여, 내담자가 문제의 원인을 알지 못하더라도 정서적 방출을 먼저 경험하게 함으로써 안전하고 점진적인 통합을 돕는 해리 기법이다.",
    "ERICKSON_IDEOMOTOR_DYNAMICS": "신체 부위의 상반된 불수의적 움직임을 동시에 제안하여 의식적인 통제를 어렵게 만들고, 이를 통해 무의식적 반응이 실제로 일어나고 있음을 내담자에게 신체적으로 입증하는 기법이다.",
    "ERICKSON_INDIRECT_SUGGESTION": "명령이 아닌 비유나 타인의 사례를 통해 암시를 우회적으로 전달하여 내담자의 방어 기제를 무력화하고, 내담자 스스로가 그 아이디어를 창안한 것처럼 느끼게 하는 기법이다.",
    "ERICKSON_INTEGRATION_DIRECTIVE": "무의식적으로 습득한 새로운 학습 내용을 의식적인 삶과 연결하도록 강력한 임상적 지침을 제공하여, 일시적인 상태 변화가 아닌 지속적인 인격적 통합을 목표로 하는 원리이다.",
    "ERICKSON_LINGUISTIC_AMBIGUITY": "언어적 중의성이나 음운론적 모호함을 사용하여 의식을 순간적으로 혼란에 빠뜨린 후, 갑작스러운 의미의 해소를 통해 암시를 무의식 깊숙이 각인시키는 기법이다.",
    "ERICKSON_METAPHOR_AUTONOMY": "치료자가 내담자의 모든 것을 통제할 수 없음을 인정하는 '전략적 무지'를 통해 내담자에게 변화의 주도권을 넘기고, 내담자의 고유한 무의식적 능력을 신뢰하도록 만드는 기법이다.",
    "ERICKSON_METAPHOR_INSIGHT": "일상적이고 사소한 일화에서 갑작스러운 깨달음(통찰)이 발생하는 과정을 묘사하여, 내담자의 무의식이 스스로의 문제를 해결할 수 있는 핵심 아이디어를 번뜩이듯 찾아내게 돕는 기법이다.",
    "ERICKSON_METAPHOR_MODERNIZATION": "고전적이고 마법 같은 은유를 현대적인 맥락으로 재구성하여 내담자의 논리적 거부감을 줄이고, 현대인의 생활 양식에 맞는 그럴듯한 방식으로 변화의 원리를 수용하게 하는 기법이다.",
    "ERICKSON_NEGATIVE_APPROACH": "변화에 대한 직접적인 압박을 제거하고 '단순한 가능성'으로만 제시함으로써 환자의 방어적 저항을 무력화하고, 호기심 어린 탐색을 통해 스스로 변화의 문을 열게 하는 역설적 접근법이다.",
    "ERICKSON_PACING_AND_RAPPORT": "내담자의 사회적 신분이나 방어적인 페르소나를 있는 그대로 수용하고 평범하게 반응함으로써 불필요한 권력 투쟁을 피하고 안정적인 심리적 유대감을 형성하는 기초 기법이다.",
    "ERICKSON_PACING_AND_VALIDATION": "내담자의 현재 반응이나 감각적 경험을 즉각적으로 언어화하여 거울처럼 반영함으로써, 내담자가 치료자에 대해 깊은 신뢰와 안전함을 느끼게 하여 트랜스 상태를 공고히 하는 기법이다.",
    "ERICKSON_PARADOXICAL_IMPLICATION": "현재의 의식적인 노력을 '힘든 과업'으로 재정의하여 피로감을 유도하고, 그 반대 급부인 트랜스나 수면 상태를 자연스럽고 환영받는 안식으로 인식하게 만드는 역설적 암시 기법이다.",
    "ERICKSON_PERMISSIVE_RELAXATION": "강압적인 명령 대신 '당신이 원하는 만큼'과 같은 허용적인 언어를 사용하여 내담자에게 통제권을 부여하고, 무의식이 스스로의 속도에 맞춰 깊은 이완 상태로 진입하도록 돕는 기법이다.",
    "ERICKSON_POSTHYPNOTIC_VALIDATION": "트랜스 상태에서 부여된 암시가 일상에서 실제로 실행되고 있음을 입증하고 설명함으로써, 무의식이 시간이 지난 후에도 지시를 충실히 수행하는 강력한 실행체임을 확인시키는 기법이다.",
    "ERICKSON_PRESUPPOSITION": "변화가 일어날 것임을 문법적으로 당연하게 전제하여 내담자의 주의를 '변화의 방식'으로 돌림으로써, 내담자가 질문에 답하는 동안 무의식적으로 변화를 사실로 받아들이게 하는 기법이다.",
    "ERICKSON_RAPPORT_BOUNDARY": "치료자와 내담자 사이의 배타적인 심리적 공간을 설정하고 외부의 간섭을 차단함으로써, 내담자가 외부 시선에서 자유로워져 오직 자신의 내면적 탐색에만 집중할 수 있게 돕는 기법이다.",
    "ERICKSON_REFRAMING": "고착된 문제나 고통을 '지혜로운 스승'이나 '학습의 기회'로 재정의하여 사건의 의미를 완전히 바꿈으로써, 모든 부정적 경험을 성장을 위한 긍정적 자원으로 전환시키는 핵심 기법이다.",
    "ERICKSON_REFRAMING_CONFRONTATION": "내담자가 겪고 있는 고통을 강력하고 명확한 도덕적/논리적 프레임으로 규정하여 내담자의 억울함을 인정하는 동시에, 상황을 치료자가 완전히 장악하고 있음을 보여주어 심리적 안정감을 주는 기법이다.",
    "ERICKSON_REFRAMING_POSSIBILITY": "내담자의 경직된 논리에 의문을 제기하고 상반된 속성이 동시에 존재할 수 있음을 제안하여, 좁은 문제 상황 속에서도 새로운 가능성과 개방성을 발견하도록 돕는 인지적 재구조화 기법이다.",
    "ERICKSON_REFRAMING_UTILIZATION": "내담자의 요청이나 불평을 치료적 주도권을 확보하기 위한 '활용'의 기회로 전환하고, 상황을 역설적으로 재정의하여 내담자의 주의를 즉각적으로 환기시키고 정서적 유대를 강화하는 기법이다.",
    "ERICKSON_SYMBOLIC_GROWTH_TASK": "슬픔이나 정체를 상징하는 대상에 성장의 의미를 부여하고 이를 지켜보는 구체적인 과업을 할당하여, 내담자의 심리에너지가 고통스러운 과거에서 역동적인 미래로 자연스럽게 흐르도록 돕는 기법이다.",
    "ERICKSON_TIME_DISTORTION_VALIDATION": "트랜스 상태에서의 주관적 시간과 실제 시간의 괴리를 내담자에게 확인시켜 무의식적 변화의 깊이를 실감하게 하고, 이를 통해 치료적 성과를 의식 차원에서 강력하게 공고히 하는 기법이다.",
    "ERICKSON_TIME_DOUBLE_BIND": "시간을 충분히 갖는 것과 빠르게 트랜스에 들어가는 것을 한 문장에 결합하여 의식적 혼란을 유도하고, 무의식이 가장 효율적인 방식으로 트랜스를 수용하도록 유도하는 이중 구속 기법이다.",
    "ERICKSON_TRANCE_DESCRIPTION": "대상의 주관적 현실이 일상과 멀어져 있음을 정의하고 내면 세계의 경계를 설정함으로써, 주의력의 협착이라는 트랜스의 특징을 강화하고 그 상태의 주관적 진실성을 입증하는 기법이다.",
    "ERICKSON_TRUISM_CALIBRATION": "인간 행동에 대한 부정할 수 없는 보편적 진실(Truism)을 진술하여 신뢰를 구축하고, 이를 통해 내담자가 자신의 내면 상태를 스스로 교정(Calibration)하도록 유도하는 라포 강화 기법이다.",
    "ERICKSON_TRUISM_UTILIZATION": "치료자 자신의 인간적인 약점이나 명백한 사실을 솔직하게 고백하여 내담자의 방어 기제를 낮추고, 인식의 상대성을 일깨워 문제 상황을 다른 시각으로 바라볼 수 있게 돕는 기초 기법이다.",
    "ERICKSON_UNCONSCIOUS_PROCESS": "치료의 목표를 개인적 성장으로 재설정하고 과정 중심의 동사를 사용하여, 의식적인 불안이나 강박 없이 무의식이 자연스럽게 정보를 통합하고 변화를 이끌어내도록 돕는 원리이다.",
    "ERICKSON_UTILIZATION_AND_EXCLUSION": "특정한 시각적 형상이나 인상에 강력하게 집중하게 함으로써 그 외의 현실을 일시적으로 지워버리는 '부정적 환각' 원리를 활용하여, 최면의 깊이를 심화하고 암시의 집중도를 높이는 기법이다.",
    "ERICKSON_UTILIZATION_PUN": "주변의 예기치 않은 자극이나 환경적 변화를 유머러스한 중의적 표현으로 재정의하여 치료적 과정에 흡수함으로써, 어떤 외부적 요소도 치료의 흐름을 방해할 수 없음을 보여주는 활용 기법이다.",
    "ERICKSON_UTILIZATION_REFRAMING": "내담자가 보이는 무반응이나 무능력을 오히려 새로운 가치를 창출할 수 있는 독특한 기회로 재정의하여, 내담자를 '치료 대상'에서 '모두를 가르칠 수 있는 스승'으로 격상시키는 리프레이밍 기법이다."
}

def update_dna_logic():
    if not os.path.exists(DNA_FILE):
        print(f"Error: {DNA_FILE} not found.")
        return

    with open(DNA_FILE, 'r', encoding='utf-8') as f:
        dna_data = json.load(f)

    updated_count = 0
    for situation in dna_data:
        for entry in dna_data[situation]:
            pid = entry.get('pattern_id')
            if pid in UNIVERSAL_LOGIC:
                entry['logic'] = UNIVERSAL_LOGIC[pid]
                updated_count += 1

    with open(DNA_FILE, 'w', encoding='utf-8') as f:
        json.dump(dna_data, f, ensure_ascii=False, indent=4)

    print(f"Successfully updated {updated_count} entries with universal strategic logic.")

if __name__ == "__main__":
    update_dna_logic()
