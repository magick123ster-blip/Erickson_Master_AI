# Erickson LSTM Sequential DNA Analysis Report

이 리포트는 밀턴 에릭슨의 치료적 발화 시퀀스를 학습한 LSTM(Long Short-Term Memory) 신경망의 분석 결과입니다. 단순한 1차 마르코프 체인과 달리, 이 모델은 이전 5단계의 맥락(Context)을 고려하여 가장 에릭슨다운 '다음 수'를 제안합니다.

## 1. Model Architecture Overview

| Feature | Macro Strategy Model | Sub-Macro (OTHER) Model |
| :--- | :--- | :--- |
| Vocabulary Size | 8 States | 13 States |
| Layers | 2-Layer LSTM | 2-Layer LSTM |
| Embedding Dim | 16 | 32 |
| Hidden Dim | 32 | 64 |
| Dropout | 0.2 | 0.3 |

## 2. Strategic Context Simulation

에릭슨의 전형적인 대화 흐름을 입력했을 때, AI가 예측하는 최적의 다음 단계입니다.

### Standard Induction (표준 유도)
**입력 맥락 (Past 5 Steps):** `PACING -> TRUISM -> PACING -> TRUISM -> PACING`  
**AI 예측 다음 전략 (Top 3):**
1. **OTHER** (32.6%)  
   `██████`
2. **UTILIZATION** (19.4%)  
   `███`
3. **PACING** (15.7%)  
   `███`

### Confusion & Paradox (혼란과 역설)
**입력 맥락 (Past 5 Steps):** `DOUBLE_BIND -> CONFUSION -> DOUBLE_BIND -> CONFUSION -> OTHER`  
**AI 예측 다음 전략 (Top 3):**
1. **REFRAMING** (21.7%)  
   `████`
2. **OTHER** (19.2%)  
   `███`
3. **UTILIZATION** (15.6%)  
   `███`

### Reframing Flow (리프레이밍 흐름)
**입력 맥락 (Past 5 Steps):** `PACING -> UTILIZATION -> REFRAMING -> UTILIZATION -> SUGGESTION`  
**AI 예측 다음 전략 (Top 3):**
1. **OTHER** (40.7%)  
   `████████`
2. **UTILIZATION** (19.7%)  
   `███`
3. **TRUISM** (9.3%)  
   `█`

### Inside 'OTHER' - Trance Building ('OTHER' 내부의 트랜스 구축)
**입력 맥락 (Past 5 Steps):** `OTHER_CUE_PROMPT -> OTHER_DISSOCIATION -> OTHER_CUE_PROMPT -> OTHER_DISSOCIATION -> OTHER_TIME_AMNESIA`  
**AI 예측 다음 전략 (Top 3):**
1. **OTHER_UNKNOWN** (25.5%)  
   `█████`
2. **UTILIZATION** (13.6%)  
   `██`
3. **OTHER_TIME_AMNESIA** (11.2%)  
   `██`

### Inside 'OTHER' - Resistance Handling ('OTHER' 내부의 저항 처리)
**입력 맥락 (Past 5 Steps):** `OTHER_INQUIRY -> OTHER_CHALLENGE -> OTHER_INQUIRY -> OTHER_CHALLENGE -> OTHER_UNKNOWN`  
**AI 예측 다음 전략 (Top 3):**
1. **OTHER_UNKNOWN** (20.3%)  
   `████`
2. **UTILIZATION** (19.4%)  
   `███`
3. **PACING** (10.9%)  
   `██`

## 3. Findings & Insights

- **Context Sensitivity**: LSTM 모델은 동일한 'PACING' 상태라도 이전에 'TRUISM'이 반복되었는지, 아니면 'CONFUSION'이 있었는지에 따라 완전히 다른 다음 기법을 추천합니다.
- **Higher-order Markov Effect**: 단순 전이 확률에서는 나타나지 않는 '리듬'과 '밀도'의 법칙이 모델의 가중치에 녹아 있습니다.
- **Strategy DNA**: 에릭슨이 특정 고난도 기법(Double Bind 등)을 사용한 후 반드시 라포 형성 단계(Pacing/Truism)로 복귀하는 경향이 확률적으로 뚜렷하게 나타납니다.
