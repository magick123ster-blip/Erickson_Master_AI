import pandas as pd
import os

DATA_DIR = r'C:\Users\magic\Downloads\erickson_data'
SOURCE_CSV = os.path.join(DATA_DIR, 'hierarchical_report_source.csv')
OUTPUT_MD = os.path.join(DATA_DIR, 'full_erickson_encyclopedia.md')

def generate_markdown():
    df = pd.read_csv(SOURCE_CSV)
    
    with open(OUTPUT_MD, 'w', encoding='utf-8') as f:
        f.write("# 밀턴 에릭슨 전략 패턴 전수 백과사전 (Full-Spectrum Encyclopedia)\n\n")
        f.write("본 보고서는 분석된 모든 3,361개의 유니크한 패턴과 6,490개의 전이 관계를 계층적으로 정리한 무손실 리포트입니다.\n\n")
        
        f.write("## 전략적 카테고리 목차\n")
        categories = sorted(df['Category'].unique())
        for cat in categories:
            count = len(df[df['Category'] == cat])
            f.write(f"- [{cat}](#{cat.lower()}) ({count}개 패턴)\n")
        f.write("\n---\n\n")
        
        for cat in categories:
            f.write(f"## {cat}\n\n")
            cat_df = df[df['Category'] == cat].sort_values(by='Importance', ascending=False)
            
            f.write("| 중요도 | 패턴 ID | 다음 단계 (Leads To) | 이전 단계 (Preceded By) |\n")
            f.write("| :--- | :--- | :--- | :--- |\n")
            
            for _, row in cat_df.iterrows():
                # Format importance to scientific notation if very small
                imp = f"{row['Importance']:.6f}" if row['Importance'] > 0.000001 else f"{row['Importance']:.2e}"
                
                f.write(f"| {imp} | `{row['Pattern ID']}` | {row['Typical Leads To']} | {row['Typical Preceded By']} |\n")
            
            f.write("\n\n")

    print(f"Encyclopedia generated at {OUTPUT_MD}")

if __name__ == "__main__":
    generate_markdown()
