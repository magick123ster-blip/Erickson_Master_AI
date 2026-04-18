# 에릭슨 인지 스키마 추출 및 뇌 지도 그리기 계획

이 계획은 에릭슨의 치료 데이터에서 무의식적인 정보 처리 과정(스키마)을 추출하고 시각화하는 과정을 가이드합니다.

## 목표
1. **의사결정 트리 (Decision Tree) 생성**: `맥락(Context)`과 `추론(Reasoning)`을 입력으로 하여 에릭슨의 판단 규칙(IF-THEN-BECAUSE)을 추출합니다.
2. **군집화 (Clustering)를 통한 핵심 프레임 도출**: 방대한 추론 데이터를 10-15개의 핵심 인지 프레임으로 압축합니다.
3. **핵심 언어 장치 추출 (NLP)**: 에릭슨 특유의 암시적 동사, 수동태 구조, 이중 구속용 접속사 등을 분석합니다.
4. **전체 POS 태깅**: 7,900개 전 문장의 모든 단어에 품사 태그(POS Tag)를 부여하여 저장합니다.
5. **의존 구문 분석 (Syntax Tree Analysis)**: 단어 간의 수식 관계, SVO 구조 등을 분석하여 에릭슨 특유의 문장 구성 법칙을 도출합니다.
6. **N-gram 및 연어(Collocation) 분석**: 2~4개 단어 조합의 빈도와 함께 나타나는 단어들의 통계적 연관성을 분석합니다.
7. **의미역 태깅 (Semantic Role Labeling)**: 문장의 술어를 중심으로 누가(Agent), 무엇을(Patient), 어떻게(Manner), 어디서(Location) 등의 의미론적 구조를 추출합니다.
8. **빈발 부분 트리 마이닝 (Frequent Subtree Mining)**: 의존 구문 분석 결과를 트리 정규화하여 에릭슨 발화의 반복적인 문형 템플릿(Rhetorical Templates)을 추출합니다.
9. **토픽 모델링 (Topic Modeling)**: LDA 알고리즘을 사용하여 전체 발화 데이터에서 반복적으로 나타나는 핵심 주제(Topics)와 키워드 군집을 식별합니다.
10. **연관 규칙 마이닝 (Association Rule Mining)**: 맥락(Context), 추론(Reasoning), 출력(Output) 사이의 상관관계를 Apriori/FP-Growth 알고리즘으로 분석하여 "IF 맥락/추론 THEN 출력"의 법칙을 도출합니다.

## 제안된 변경 사항

### [NEW] schema_extraction.py (기능 추가 또는 별도 스크립트)
(기존 스키마 추출 기능 포함)

### [NEW] linguistic_analysis.py
에릭슨의 발화 데이터(`output`)를 분석하는 NLP 스크립트:
- **암시적 동사 추출**: `wonder`, `discover`, `notice`, `allow` 등 변화를 유도하는 동사의 빈도 분석.
- **수동태 및 주어 생략 구조 분석**: `it can be noticed`와 같이 책임을 모호하게 하는 수동태 패턴 감지.
- **이중 구속 및 연쇄 구조**: `either... or`, `whether... or` 등 선택의 자유를 제한하면서도 부여하는 접속사 사용 패턴 분석.

## 검증 계획

### 자동화 테스트
- **추출 품질 검사**: 군집화 결과(Silhouette Score 등)를 통해 데이터 압축의 적절성 확인.
- **언어 장치 탐지 정확도**: spaCy의 의존성 파싱 결과를 통해 수동태 및 특정 구문 탐지의 정확도 확인.

### 수동 검증
- 추출된 IF-THEN-BECAUSE 규칙이 실제 에릭슨의 치료 원칙(Utilisation, Confusion 등)과 일치하는지 임상적 검토.
- 10-15개의 핵심 프레임이 중복 없이 에릭슨의 기술을 포괄하는지 확인.
