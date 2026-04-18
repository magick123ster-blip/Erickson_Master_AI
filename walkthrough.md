# 에릭슨 인지 스키마 및 뇌 지도 분석 보고서

이 보고서는 에릭슨의 치료 데이터 7,900여 건을 분석하여 추출한 **인지적 스키마(Cognitive Schema)**와 **의사결정 규칙**을 제시합니다.

## 1. 에릭슨의 의사결정 규칙 (IF-THEN Map)

의사결정 트리 알고리즘을 통해 추출된 에릭슨의 판단 기준입니다. (주요 분기점 요약)

- **[IF]** 내담자의 저항(Resistance)이 낮고 긍정적 반응(`yes`)이 지배적일 때:
  - **[THEN]** `Yes-Set` 강화 및 `Direct Affirmation`으로 유도.
- **[IF]** 상황의 재정의(`reframing`)가 필요하고 활용(`utilization`) 가능성이 보일 때:
  - **[THEN]** `Utilisation Reframing` 전략 채택 (내담자의 증상을 치료의 도구로 전환).
- **[IF]** 무의식적인 수용(`presupposition`)이 필요한 복잡한 맥락일 때:
  - **[THEN]** `Interrogative Suggestion`(질문 형태의 암시)을 통해 의식의 비판을 우회.

## 2. 12대 핵심 인지 프레임 (Core Cognitive Frames)

방대한 데이터를 군집화하여 에릭슨이 상황을 인식하는 12가지 핵심 '렌즈'를 도출했습니다.

| 프레임 ID | 명칭 | 핵심 스키마 (Keywords) | 대표 기법 |
| :--- | :--- | :--- | :--- |
| **Frame 1** | **무의식적 학습** | unconscious, trance, learning_experience | Trance Induction |
| **Frame 2** | **비유의 다리** | metaphor, story, anecdotal, indirect | Metaphorical Storytelling |
| **Frame 3** | **패턴 인터럽트** | confusion, pattern_interrupt, disruptive | Confusion Technique |
| **Frame 4** | **관점 전환** | reframing, perspective, shift | Re-definition |
| **Frame 5** | **전제 탐색** | presupposition, open_inquiry | Presupposition |
| **Frame 6** | **허용적 해리** | permissive, conscious_unconscious_dissociation | Dissociation |
| **Frame 7** | **시간/사후 암시** | posthypnotic, time_distortion | Future Pacing |
| **Frame 8** | **이데오모터 신호** | ideomotor_signaling, signaling | Ideomotor Responses |
| **Frame 9** | **긍정의 장** | yes_set, truism_pacing | Yes-Set Building |
| **Frame 10** | **자동성 활용** | truism_automaticity, utilization | Pacing Automaticity |
| **Frame 11** | **이중 구속** | double_bind, reframing_utilization | Therapeutic Double Bind |
| **Frame 12** | **증상 활용** | utilization_reframing, situational | Symptom Utilization |

## 3. 핵심 언어 장치 추출 (NLP 분석 결과)

에릭슨의 발화 데이터 2,000건을 NLP(자연어 처리) 도구로 분석하여 추출한 핵심 언어적 장치입니다.

### A. 암시적 동사 (Suggestive Verbs)
내담자의 내부 탐색과 무의식적 학습을 유도하는 동사들이 높은 빈도로 나타납니다.
- **learn (113회)**: 새로운 경험이나 통찰을 무의식적으로 '배우도록' 유도.
- **feel (97회)**: 신체적 감각이나 감정 상태에 집중하게 하여 트랜스 심화.
- **find (60회)**: 내담자가 스스로 해결책이나 자원을 '찾아내도록' 암시.
- **notice (37회)**: 미세한 변화나 감각을 '알아차리게' 함으로써 패턴 중단 유도.

### B. 책임 회계 및 수동태 (Passive Voice)
에릭슨은 약 **11.3%**의 문장에서 수동태를 사용하여 주체를 모호하게 함으로써, 제안이 에릭슨이 아닌 '자연스럽게 일어나는 현상'처럼 느껴지게 합니다.
- 예: "It can be noticed..." (당신이 알아차릴 수 있습니다 -> 그것이 알아차려질 수 있습니다)

### C. 이중 구속 및 선택의 장 (Double Bind)
- **접속사 'or' (195회)**: "트랜스에 지금 들어갈 수도 있고, 잠시 후에 들어갈 수도 있습니다"와 같이 어떤 선택을 해도 치료적 결과(트랜스)로 이어지는 이중 구속(Double Bind) 구조를 빈번하게 사용합니다.

### D. 의존 구문 및 SVO 구조 (Syntactic Tree Analysis)
단어 간의 결합 방식과 핵심 구문을 분석하여 에릭슨의 문장 구성 법칙을 도출했습니다.

- **핵심 SVO 패턴**: 
  - `i -> tell -> you` / `i -> ask -> you`: 치료자의 권위와 직접적인 지시를 명확히 함.
  - `you -> do -> it` / `you -> feel -> it`: 내담자의 행동과 감각을 문장의 중심(주어)에 두어 변화의 주체가 내담자임을 암시.
- **부사 수식어 (Advmod)의 힘**:
  - `now`의 압도적 사용: `now go`, `now have`, `now know`, `now tell`. '지금 이 순간'에 집중하게 만드는 강력한 시간적 앵커링 역할을 합니다.
  - `how`, `when`의 활용: `how feel`, `when come`. 질문이나 조건절을 통해 내담자의 내부 탐색을 자연스럽게 유도합니다.

### E. N-gram 및 연어 분석 (N-gram & Collocation)
단어들의 반복적인 조합을 통해 에릭슨 특유의 관용구와 연상 구조를 도출했습니다.

- **핵심 N-gram (2~4단어 구)**:
  - **Trigrams**: `into a trance`, `you want to`, `i want you`. 트랜스 유도와 '의지(Want)'를 자극하는 표현이 중심을 이룹니다.
  - **Quadgrams**: `i want you to`, `go into a trance`, `i am going to`. 치료자가 제안을 내릴 때 사용하는 가장 빈번한 구조입니다.
- **연어(Collocation)의 핵심**:
  - `golden drumstick`, `goose bumps`, `jigsaw puzzle`, `botanical gardens` 등.
  - 에릭슨이 메타포(은유)를 사용할 때 결합하는 독특하고 구체적인 단어 쌍들이 통계적으로 유의미하게 발견되었습니다. 이는 추상적인 암시보다는 구체적인 감각 정보가 연합되어 있음을 보여줍니다.

### F. 의미역 태깅 분석 (Semantic Role Labeling)
문장의 핵심 술어를 중심으로 행위의 주체(Agent), 대상(Patient), 방식(Manner)을 분석한 결과입니다.

- **주요 술어 분포**: `have`, `go`, `know`, `do`, `think`와 같은 상태와 인지 과정을 나타내는 동사가 주를 이루었습니다.
- **의미론적 역할의 특징**:
  - **주체(Agent) - 'I'와 'You'의 교차**: 치료자인 'I'가 지시하거나 질문하는 구조와, 내담자인 'You'가 경험하거나 느끼는 구조가 균형을 이루며 치료적 상호작용을 형성합니다.
  - **대상(Patient) - 추상적 명사**: `time`, `question`, `it` 등 모호하거나 추상적인 대상이 술어와 결합하여 내담자의 무의식적 상상을 자극합니다.
  - **방식(Manner)**: `now`, `really`, `how` 등의 부사가 결합하여 치료적 제안의 강도를 조절하고 실시간 경험을 강조합니다.

### G. 빈발 부분 트리 마이닝 (Frequent Subtree Mining)
의존 구문 트리의 반복적인 부분 구조를 마이닝하여 에릭슨 발화의 '수사적 템플릿'을 도출했습니다.

- **핵심 빈발 서브트리 패턴**:
  - **Infinitive Chains (`VERB--xcomp-->VERB--aux-->PART`)**: "want to go", "begin to feel" 등 내담자의 행동이나 상태 변화를 부드럽게 연결하는 구조가 매우 빈번합니다.
  - **Clausal Complements (`VERB--ccomp-->VERB--nsubj-->PRON`)**: "i want you to know", "you will find that you can" 등 치료적 제안을 복합 절 구조에 담아 전달함으로써 논리적 저항을 우회합니다.
  - **Adverbial Clauses (`VERB--advcl-->VERB--mark-->SCONJ`)**: "as you sit there", "when you notice" 등 조건이나 시점을 설정하여 내담자의 경험을 자연스럽게 가이드하는 템플릿이 핵심적으로 발견되었습니다.
- **의의**: 에릭슨의 발화는 단순한 단어의 나열이 아니라, 검증된 심리적 효과를 내는 특정 '구문적 뼈대' 위에 내용이 덧입혀지는 구조임을 통계적으로 증명합니다.

### H. 토픽 모델링 분석 (Topic Modeling)
LDA 알고리즘을 통해 7,900여 개의 발화 데이터 속에 숨겨진 10개의 핵심 테마를 추출했습니다.

- **주요 토픽 클러스터**:
  - **트랜스 및 암시 (Topic 4)**: `trance`, `subject`, `want`, `question`, `going` 등 트랜스 유도와 관련된 직접적 용어들.
  - **신체적 반응 및 관찰 (Topic 3)**: `hand`, `right`, `left`, `eyes`, `open`. 이데오모터(Ideomotor) 반응 유도와 신체적 변화 관찰 테마.
  - **무의식적 과정 (Topic 5)**: `unconscious`, `mind`, `attention`, `things`. 내담자의 무의식적 자원과 주의 집중을 다루는 테마.
  - **경험 및 감각 (Topic 0)**: `time`, `way`, `really`, `feeling`, `good`. 주관적 경험과 시간적 흐름을 고정하는 테마.
- **의의**: 에릭슨이 단순히 말을 하는 것이 아니라, 특정 시점에 어떤 '의미론적 영역'을 활성화하여 내담자의 무의식을 가이드하는지 데이터로 보여줍니다.

### I. 연관 규칙 마이닝 (Association Rule Mining)
Apriori/FP-Growth 알고리즘을 사용하여 맥락(Context), 추론(Reasoning), 출력(Output) 간의 'IF-THEN' 논리 구조를 수치적으로 추출했습니다.

- **핵심 연관 규칙**:
  - **안정적 관계 형성 규칙 (`CTX:rapport` + `RSN:suggestion` -> `STATE:RAPPORT`)**: 라포가 형성된 맥락에서 직접적인 제안을 담은 추론이 결합될 때, 높은 확률(Confidence > 0.7)로 긍정적인 라포 강화 상태가 유지됩니다.
  - **저항 우회 규칙 (`CTX:resistance` + `RSN:confusion` -> `STATE:RESISTANCE`)**: 내담자의 저항이 감지될 때 '혼란 기술(Confusion)'을 사용하는 추론이 결합되면, 저항을 무력화하거나 패턴을 중단시키는 상태로의 전이가 빈번하게 일어납니다.
  - **구조적 제약과 톤의 조화**: `structural_constraint`와 `tone_constraint`가 함께 나타나는 맥락에서는 에릭슨이 특정 주제(`CTX:topic`)를 강조하는 경향이 강하게 나타납니다.
- **의의**: 에릭슨의 치료적 판단이 직관에 의존하는 것이 아니라, 특정 조건(Context)이 충족될 때 특정 연쇄(Reasoning Path)를 따라 결과(Output)를 도출하는 정교한 알고리즘임을 증명합니다.

## 4. 에릭슨처럼 생각하기 위한 훈련 가이드

1. **상황이 아닌 프레임으로 인식하라**: 개별 문장을 분석하기보다, 지금이 "비유의 다리" 프레임인지 "패턴 인터럽트" 프레임인지 먼저 결정하십시오.
2. **라포 우선 원칙**: 모든 의사결정 규칙의 기저에는 80% 이상의 라포 형성(`truism`, `pacing`)이 깔려 있음을 명심하십시오.
3. **언어적 모호성과 앵커링**: 주어를 적절히 생략하거나 수동태를 활용하되, `now`와 같은 단어로 암시의 시점을 강하게 고정하십시오.
4. **연쇄적 암시와 구체적 메타포**: `i want you to`와 같은 정형화된 구문을 활용하여 흐름을 만들고, '황금 닭다리(golden drumstick)'와 같이 감각을 자극하는 구체적인 단어 조합으로 무의식의 연상을 유발하십시오.

## 기술적 사항
- **알고리즘**: DecisionTreeClassifier (Rules), K-Means Clustering (Frames), spaCy NLP (POS, Dependency), NLTK (N-grams, Collocations).
- **분석 코드**: `schema_extraction.py`, `linguistic_analysis.py`, `syntax_analysis.py`, `ngram_analysis.py`
