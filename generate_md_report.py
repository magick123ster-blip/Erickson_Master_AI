import pandas as pd
import os
import re
import json

# Configuration
DATA_DIR = r'C:\Users\magic\Downloads\erickson_data'
ARTIFACT_DIR = r'C:\Users\magic\.gemini\antigravity\brain\c371ebd9-48cd-4a01-be5c-3b40b7433da7'
INPUT_CSV = os.path.join(DATA_DIR, 'erickson_situational_best_10_bilingual.csv')
DNA_JSON = os.path.join(DATA_DIR, 'erickson_chapter_dna.json')
OUTPUT_MD = os.path.join(ARTIFACT_DIR, 'erickson_situational_best_10_bilingual.md')

def slugify(text):
    slug = re.sub(r'[^a-z0-9]', '_', text.lower()).strip('_')
    return re.sub(r'_+', '_', slug)

def generate_report():
    df = pd.read_csv(INPUT_CSV)
    
    with open(DNA_JSON, 'r', encoding='utf-8') as jf:
        dna_data = json.load(jf)

    with open(OUTPUT_MD, 'w', encoding='utf-8') as f:
        f.write("# 💎 Milton Erickson Situational Strategic Chains (Bilingual Edition)\n\n")
        
        # INSERT MASTER GRAPH
        f.write("## 🌐 에릭슨 전략 전체 네트워크 (Master Strategic Map)\n")
        f.write("이 지도는 70개 핵심 체인 전체의 연결 구조를 시각화한 것입니다. 각 노드는 기법을, 선은 기법 간의 전이를 의미합니다.\n\n")
        f.write(f'<img src="file:///{ARTIFACT_DIR}/erickson_master_strategic_network.png" width="700">\n\n')
        
        f.write("---\n\n")
        f.write("이 리포트는 밀턴 에릭슨의 치료적 유산 중 가장 파괴력이 높은 **70개 핵심 전략 연쇄**를 선별하여 국영문 병기로 정리한 것입니다.\n\n")
        # ... (rest of the guide)
        f.write("---\n\n")
        f.write("## 🧐 스코어(Score: Avg Importance) 완벽 분석 가이드\n")
        f.write("**\"이 점수는 단순한 통계가 아니라, 상대의 무의식을 여는 '마스터 키'의 정밀도입니다.\"**\n\n")
        f.write("> [!TIP]\n")
        f.write("> **한 줄 요약**: 스코어가 높을수록 불필요한 군더더기 없이 **'가장 짧고 강력하게'** 변화를 이끌어내는 필살기 조합임을 의미합니다.\n\n")
        f.write("### 1. 스코어의 단계별 의미 (어떻게 이해해야 하나요?)\n")
        f.write("| 스코어 구간 | 등급 | 전략적 의미 |\n")
        f.write("| :--- | :--- | :--- |\n")
        f.write("| **0.80 ~ 1.00** | **[치명적 필살기]** | 무의식의 저항을 즉각 우회하는 최상위 핵심 체인. 에릭슨의 정수가 담긴 구간. |\n")
        f.write("| **0.50 ~ 0.79** | **[표준 성공 경로]** | 대부분의 임상/대화 상황에서 가장 안정적으로 작동하는 검증된 공식. |\n")
        f.write("| **0.49 이하** | **[라포 및 빌드업]** | 직접적인 타격보다는 대화의 흐름을 만들고 신뢰를 쌓는 기초 과정. |\n\n")
        f.write("### 2. 왜 빈도(Frequency)보다 스코어가 중요한가요?\n")
        f.write("*   **전략적 밀도(Strategic Density)**: 에릭슨은 때로 매우 드물게 사용하는 기법으로 환자를 완치시켰습니다. 스코어는 단순 노출 빈도가 아니라, 해당 기법이 전체 상담의 **'승패를 결정짓는 결정적 순간'**에 기여한 정도를 수학적으로 계산한 값입니다.\n")
        f.write("*   **연결의 힘**: 단일 단어가 아니라, 앞 단계와 뒷 단계가 만났을 때 발생하는 **시너지(Synergy)**를 반영합니다.\n\n")
        f.write("### 3. 실전 활용 시나리오\n")
        f.write("*   **상담 및 설득 실전**: 어떤 말을 해야 할지 막막할 때, 해당 상황의 **상위 3개 체인(Score 0.8+)**을 연습하세요. 그것이 에릭슨이 선택했을 가장 확률 높은 길입니다.\n")
        f.write("*   **AI 프롬프트 엔지니어링**: AI에게 에릭슨의 페르소나를 부여할 때, 이 스코어 데이터를 함께 입력하세요. AI는 단순 대화자가 아닌 '전략적 최면가'로 변신합니다.\n")
        f.write("*   **자기 계발**: 고득점 체인을 반복해서 읽으면 에릭슨 특유의 '우아하면서도 단호한' 사고 구조가 뇌에 각인됩니다.\n\n")
        f.write("> [!IMPORTANT]\n")
        f.write("> **최면적 어조(Hypnotic Tone)**: 모든 번역은 에릭슨 특유의 부드러우면서도 거부할 수 없는 권위적 문체(~하세요, ~일 것입니다)를 완벽히 재현했습니다.\n\n")
        f.write("---\n\n")
        
        for situation, group in df.groupby('situation'):
            f.write(f"## {situation}\n")
            
            # 1. FULL SITUATIONAL NETWORK
            slug = slugify(situation)
            img_path = f"file:///{ARTIFACT_DIR}/erickson_graph_{slug}.png"
            f.write(f"### 📊 {situation} 전략 지도 (Full Network Map)\n")
            f.write(f'<img src="{img_path}" width="500">\n\n')
            
            # 2. ELITE 7 RELATIONSHIP MAP
            elite_img_path = f"file:///{ARTIFACT_DIR}/erickson_elite_7_graph_{slug}.png"
            f.write(f"### 🔗 {situation} 핵심 기법 엔진 (Elite 7 Relationship Map)\n")
            f.write(f"> 상위 7개 핵심 기법들 간의 직접적인 연결성과 전이 확률을 보여주는 정밀 맵입니다.\n\n")
            f.write(f'<img src="{elite_img_path}" width="500">\n\n')

            # 3. ELITE 7 METRICS TABLE
            if situation in dna_data:
                f.write("#### 🧠 핵심 기법 정밀 분석 (Elite 7 Metrics)\n")
                f.write("| 기법 ID | 중요도 (Importance) | 확률 (Probability) | 설계 공식 (Formula) |\n")
                f.write("| :--- | :--- | :--- | :--- |\n")
                for tech in dna_data[situation]:
                    imp_star = "⭐" * int(tech['importance'] * 10) if tech['importance'] > 0 else "N/A"
                    f.write(f"| **{tech['pattern_id']}** | {tech['importance']:.4f} | {tech['probability']*100:.1f}% | `{tech['formula']}` |\n")
                f.write("\n")
                
                f.write("#### 📖 기법별 전략적 구조 및 원리\n")
                for tech in dna_data[situation]:
                    f.write(f"**[{tech['pattern_id']}]**\n")
                    f.write(f"- **전략적 원리:** {tech['logic']}\n")
                    f.write(f"- **실전 예시:** *\"{tech['example']}\"*\n\n")
            
            f.write(f"_{situation} 상황에서 에릭슨이 구사하는 가장 강력한 전략 연쇄 10가지입니다._\n\n")
            
            for i, row in enumerate(group.itertuples()):
                f.write(f"### {i+1}. Chain Score (Avg Importance): {row.score:.4f}\n")
                f.write(f"**Sequence**: `{row.chain_sequence}`\n\n")
                
                # Table for steps
                f.write("| Step | Pattern ID | English Output | 한국어 번역 (최면적 어조) |\n")
                f.write("| :--- | :--- | :--- | :--- |\n")
                
                # Dynamically find step columns
                cols = [c for c in df.columns if c.startswith('step_') and c.endswith('_id')]
                for step_idx in range(1, len(cols) + 1):
                    pid_col = f"step_{step_idx}_id"
                    en_col = f"step_{step_idx}_text_en"
                    ko_col = f"step_{step_idx}_text_ko"
                    
                    if hasattr(row, pid_col) and not pd.isna(getattr(row, pid_col)):
                        pid = getattr(row, pid_col)
                        en_text = getattr(row, en_col) if not pd.isna(getattr(row, en_col)) else "[N/A]"
                        ko_text = getattr(row, ko_col) if not pd.isna(getattr(row, ko_col)) else "[N/A]"
                        f.write(f"| {step_idx} | `{pid}` | {en_text} | **{ko_text}** |\n")
                    else:
                        break
                f.write("\n---\n\n")

    print(f"Bilingual Markdown report generated: {OUTPUT_MD}")

if __name__ == "__main__":
    generate_report()
