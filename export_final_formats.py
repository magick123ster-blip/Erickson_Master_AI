import pandas as pd
import os
import json
from fpdf import FPDF
from fpdf.enums import XPos, YPos

# Configuration
DATA_DIR = r'C:\Users\magic\Downloads\erickson_data'
INPUT_CSV = os.path.join(DATA_DIR, 'erickson_situational_best_10_bilingual.csv')
DNA_JSON = os.path.join(DATA_DIR, 'erickson_chapter_dna.json')
OUTPUT_TXT = os.path.join(DATA_DIR, 'erickson_situational_best_10_bilingual.txt')
OUTPUT_PDF = os.path.join(DATA_DIR, 'erickson_situational_best_10_bilingual.pdf')

def slugify(text):
    import re
    slug = re.sub(r'[^a-z0-9]', '_', text.lower()).strip('_')
    return re.sub(r'_+', '_', slug)

def export_txt():
    df = pd.read_csv(INPUT_CSV)
    with open(DNA_JSON, 'r', encoding='utf-8') as jf:
        dna_data = json.load(jf)

    with open(OUTPUT_TXT, 'w', encoding='utf-8') as f:
        f.write("=== Milton Erickson Situational Best-Chains TOP 10 (Bilingual) ===\n\n")
        f.write("이 리포트는 최고 중요도(`Importance`) 기반 70개 전략 체인의 영한 병기 버전입니다.\n\n")
        
        f.write("[Visual Assets]\n")
        f.write("- Master Map: erickson_master_strategic_network.png\n\n")
        f.write("## 💎 밀턴 에릭슨 전략 스코어(Score) 완벽 분석 가이드\n")
        f.write("\"이 점수는 단순한 통계가 아니라, 상대의 무의식을 여는 '마스터 키'의 정밀도입니다.\"\n\n")
        f.write("1. 스코어의 단계별 의미\n")
        f.write("   - [0.80 ~ 1.00] 치명적 필살기: 무의식의 저항을 즉각 우회하는 최상위 핵심 체인.\n")
        f.write("   - [0.50 ~ 0.79] 표준 성공 경로: 대부분의 상황에서 가장 안정적으로 작동하는 검증된 공식.\n")
        f.write("   - [0.49 이하] 라포 및 빌드업: 직접적인 타격보다는 대화의 흐름을 만들고 신뢰를 쌓는 기초 과정.\n\n")
        f.write("2. 왜 중요한가?\n")
        f.write("   - 전략적 밀도: 단순 빈도가 아니라, 해당 기법이 승패를 결정짓는 '결정적 순간'에 기여한 정도를 계산한 값입니다.\n")
        f.write("   - 연결의 힘: 단일 기법이 아닌, 앞뒤 단계가 만났을 때 발생하는 시너지를 반영합니다.\n\n")
        f.write("3. 활용 방법\n")
        f.write("   - 실전 상담: 어떤 말을 할지 막막할 때, 상위 3개 체인을 우선적으로 사용하세요.\n")
        f.write("   - AI 모델링: 이 스코어 데이터를 주입하면 AI가 '전략적 최면가'로 정교하게 변신합니다.\n\n")
        
        for situation, group in df.groupby('situation'):
            f.write(f"\n[{situation}]\n")
            f.write(f"Full Strategy Map: erickson_graph_{slugify(situation)}.png\n")
            f.write(f"Elite 7 Engine Map: erickson_elite_7_graph_{slugify(situation)}.png\n")
            
            if situation in dna_data:
                f.write("\n[Elite 7 Core Strategy DNA]\n")
                f.write(f"{'Pattern ID':<30} | {'Imp':<8} | {'Prob':<8}\n")
                f.write("-" * 50 + "\n")
                for tech in dna_data[situation]:
                    f.write(f"{tech['pattern_id']:<30} | {tech['importance']:.4f} | {tech['probability']*100:>6.1f}%\n")
                    f.write(f"  Formula: {tech['formula']}\n")
                    f.write(f"  Logic: {tech['logic']}\n")

            f.write("-" * 50 + "\n")
            for i, row in enumerate(group.itertuples()):
                f.write(f"\n{i+1}. Score: {row.score:.4f}\n")
                f.write(f"   Sequence: {row.chain_sequence}\n")
                
                cols = [c for c in df.columns if c.startswith('step_') and c.endswith('_id')]
                for step_idx in range(1, len(cols) + 1):
                    pid_col = f"step_{step_idx}_id"
                    en_col = f"step_{step_idx}_text_en"
                    ko_col = f"step_{step_idx}_text_ko"
                    
                    if hasattr(row, pid_col) and not pd.isna(getattr(row, pid_col)):
                        pid = getattr(row, pid_col)
                        en_text = getattr(row, en_col) if not pd.isna(getattr(row, en_col)) else "[N/A]"
                        ko_text = getattr(row, ko_col) if not pd.isna(getattr(row, ko_col)) else "[N/A]"
                        f.write(f"   - {step_idx}: {pid}\n")
                        f.write(f"      EN: {en_text}\n")
                        f.write(f"      KO: {ko_text}\n")
                    else:
                        break
    print(f"Bilingual TXT report exported: {OUTPUT_TXT}")

def export_pdf():
    df = pd.read_csv(INPUT_CSV)
    with open(DNA_JSON, 'r', encoding='utf-8') as jf:
        dna_data = json.load(jf)
    
    # PDF setup
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    
    font_reg = r'C:\Windows\Fonts\malgun.ttf'
    font_bold = r'C:\Windows\Fonts\malgunbd.ttf'
    
    if os.path.exists(font_reg):
        pdf.add_font('Malgun', '', font_reg)
        if os.path.exists(font_bold):
            pdf.add_font('Malgun', 'B', font_bold)
        font_name = 'Malgun'
    else:
        font_name = 'Arial'

    pdf.set_auto_page_break(auto=True, margin=15)
    
    # 1. Master Strategic Network (Total 70 Chains)
    pdf.add_page()
    pdf.set_font(font_name, style='B', size=20)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 15, "Milton Erickson Master Strategic Network Map", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.ln(5)
    
    master_img = os.path.join(DATA_DIR, 'erickson_master_strategic_network.png')
    if os.path.exists(master_img):
        pdf.image(master_img, x=20, y=35, w=250)
        
    # --- [NEW] TOC Placeholders ---
    toc_page_no = pdf.page_no() + 1
    pdf.add_page() # Reserve page for TOC
    toc_data = [] # To store (Situation, PageNo, LinkID)

    for situation, group in df.groupby('situation'):
        slug = slugify(situation)
        
        # Start Chapter - Track Page and Link
        link_id = pdf.add_link()
        
        # 1. FULL SITUATIONAL NETWORK
        pdf.add_page()
        chapter_start_page = pdf.page_no() # The actual page number of this new page
        toc_data.append((situation, chapter_start_page, link_id))
        
        pdf.set_link(link_id) # Set link destination to this page
        pdf.set_font(font_name, style='B', size=18)
        pdf.cell(0, 10, f"Situation Analysis: {situation}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        pdf.ln(5)
        slug = slugify(situation)
        sit_img = os.path.join(DATA_DIR, f'erickson_graph_{slug}.png')
        if os.path.exists(sit_img):
            pdf.image(sit_img, x=58, y=40, w=180)
            
        # 2. SEPARATE PAGE FOR ELITE 7 MAP
        pdf.add_page()
        pdf.set_font(font_name, style='B', size=16)
        pdf.cell(0, 10, f"🔗 {situation}: 핵심 기법 엔진 (Elite 7 Relationship Map)", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        pdf.ln(5)
        
        elite_img = os.path.join(DATA_DIR, f"erickson_elite_7_graph_{slug}.png")
        if os.path.exists(elite_img):
            pdf.image(elite_img, x=70, y=35, w=150)
            
        # 3. SEPARATE PAGE FOR DNA AND CONTENT
        pdf.add_page()
        
        # INSERT CHAPTER DNA
        if situation in dna_data:
            pdf.set_font(font_name, style='B', size=16)
            pdf.set_text_color(255, 69, 0) # Tomato color for header
            pdf.cell(0, 12, f"🧠 {situation}: 핵심 기법 정밀 분석 (Elite 7 Metrics)", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_text_color(0, 0, 0)
            
            # Draw Table Header (Optimized Widths)
            pdf.set_font(font_name, style='B', size=11)
            pdf.set_fill_color(240, 240, 240)
            pdf.cell(80, 10, " 기법 ID (Pattern ID)", border=1, fill=True)
            pdf.cell(25, 10, " 중요도", border=1, fill=True, align='C')
            pdf.cell(25, 10, " 확률", border=1, fill=True, align='C')
            pdf.cell(0, 10, " 설계 공식 (Formula)", border=1, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            
            for tech in dna_data[situation]:
                pid_text = f" {tech['pattern_id']}"
                # Dynamic Font Scaling for Long PIDs
                current_font_size = 10
                pdf.set_font(font_name, size=current_font_size)
                while pdf.get_string_width(pid_text) > 78 and current_font_size > 6:
                    current_font_size -= 0.5
                    pdf.set_font(font_name, size=current_font_size)

                pdf.cell(80, 9, pid_text, border=1)
                
                pdf.set_font(font_name, size=10) # Reset to standard for numbers
                pdf.cell(25, 9, f"{tech['importance']:.4f}", border=1, align='C')
                pdf.cell(25, 9, f"{tech['probability']*100:.1f}%", border=1, align='C')
                
                pdf.set_font(font_name, style='B', size=9)
                pdf.set_text_color(0, 102, 204)
                pdf.cell(0, 9, f" {tech['formula']}", border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.set_text_color(0, 0, 0)
                
            pdf.ln(5)
            pdf.set_font(font_name, style='B', size=12)
            pdf.cell(0, 10, "📖 기법별 전략적 구조 및 원리", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            
            for tech in dna_data[situation]:
                pdf.set_font(font_name, style='B', size=10)
                pdf.cell(0, 8, f"• {tech['pattern_id']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.set_font(font_name, size=9)
                pdf.multi_cell(0, 5, f"  Logic: {tech['logic']}")
                pdf.ln(1)
            pdf.ln(5)

        pdf.set_font(font_name, size=10)
        pdf.cell(0, 8, "Milton Erickson Situational Strategic Chains (Bilingual)", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        pdf.ln(5)
        
        # Enhanced Score Interpretation Block
        pdf.set_font(font_name, style='B', size=11)
        pdf.set_fill_color(230, 240, 255)
        pdf.cell(0, 10, "💎 스코어(Score: Avg Importance) 완벽 분석 가이드", new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True, align='C')
        pdf.set_font(font_name, size=9)
        pdf.multi_cell(0, 6, "1. [0.8+] 치명적 필살기: 무의식 저항을 즉각 우회하는 최상위 핵심 체인\n2. [0.5~0.7] 표준 성공 경로: 대부분의 상황에서 안정적으로 작동하는 검증된 공식\n3. [활용] 점수가 높을수록 에릭슨의 정수가 담긴 '가장 짧고 강력한' 변화의 길입니다.", border=1)
        pdf.ln(5)
        
        for i, row in enumerate(group.itertuples()):
            # Re-check page space
            if pdf.get_y() > 165:
                pdf.add_page()
                
            pdf.set_font(font_name, style='B', size=11)
            pdf.set_fill_color(240, 240, 240)
            pdf.cell(0, 8, f"  Chain {i+1} | Score: {row.score:.4f}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
            pdf.set_font(font_name, size=9)
            pdf.multi_cell(0, 6, f"  Sequence: {row.chain_sequence}")
            pdf.ln(2)
            
            # Step layout
            cols = [c for c in df.columns if c.startswith('step_') and c.endswith('_id')]
            for step_idx in range(1, len(cols) + 1):
                pid_col = f"step_{step_idx}_id"
                en_col = f"step_{step_idx}_text_en"
                ko_col = f"step_{step_idx}_text_ko"
                
                if hasattr(row, pid_col) and not pd.isna(getattr(row, pid_col)):
                    pid = getattr(row, pid_col)
                    en_text = getattr(row, en_col) if not pd.isna(getattr(row, en_col)) else "[N/A]"
                    ko_text = getattr(row, ko_col) if not pd.isna(getattr(row, ko_col)) else "[N/A]"
                    
                    pdf.set_font(font_name, style='B', size=9)
                    pdf.write(6, f"    Step {step_idx}: {pid}\n")
                    pdf.set_font(font_name, size=8)
                    pdf.write(6, f"      [EN] {en_text}\n")
                    pdf.set_text_color(0, 102, 204) # Subtle blue for Korean
                    pdf.set_font(font_name, style='B', size=9)
                    pdf.write(6, f"      [KO] {ko_text}\n")
                    pdf.set_text_color(0, 0, 0)
                    pdf.ln(2)
                else:
                    break
            pdf.ln(4)
    
    # --- [NEW] Generate TOC Content Retroactively ---
    pdf.page = toc_page_no
    pdf.set_y(15) # EXPLICITLY RESET Y to top of the page to avoid overlap/overflow
    pdf.set_font(font_name, style='B', size=24)
    pdf.set_text_color(255, 69, 0)
    pdf.cell(0, 20, "목차 (Table of Contents)", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.ln(10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font(font_name, size=14)
    
    for title, pg, lid in toc_data:
        pdf.set_font(font_name, style='B', size=14)
        # Situational Title (Clickable)
        pdf.cell(240, 10, f"• {title}", new_x=XPos.RIGHT, new_y=YPos.TOP, link=lid)
        
        # Page Number (Right aligned)
        pdf.set_font(font_name, size=14)
        pdf.cell(0, 10, f"P. {pg}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R')
        
        # Decorative dots (Optional but nice)
        pdf.set_draw_color(200, 200, 200)
        pdf.line(pdf.get_x() + 10, pdf.get_y(), 270, pdf.get_y()) # Simple line instead of complex dots for now
        pdf.ln(2)

    pdf.output(OUTPUT_PDF)
    print(f"Bilingual PDF report exported: {OUTPUT_PDF}")

if __name__ == "__main__":
    export_txt()
    export_pdf()
