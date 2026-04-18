import pandas as pd
import os

DATA_DIR = r'C:\Users\magic\Downloads\erickson_data'
INPUT_CSV = os.path.join(DATA_DIR, 'erickson_sequences.csv')

def find_real_examples():
    df = pd.read_csv(INPUT_CSV)
    df = df.sort_values(by=['script_id', 'turn_no'])
    
    print("# [Milton Erickson Strategic Chain Examples - 실전 사례 분석]\n")
    print("분석된 마르코프 체인 경로가 실제 에릭슨의 상담 스크립트에서 어떻게 나타나는지 확인합니다.\n")

    # 1. YES_SET -> PACING -> UTILIZATION 체인 찾기
    print("## 사례 1: 라포 및 활용 체인 (Yes-Set -> Pacing -> Utilization)")
    for name, group in df.groupby('script_id'):
        patterns = group['pattern_id'].tolist()
        contents = group['content'].tolist()
        for i in range(len(patterns)-2):
            if 'YES_SET' in patterns[i] and 'PACING' in patterns[i+1] and 'UTILIZATION' in patterns[i+2]:
                print(f"**[상담명: {name}]**")
                print(f"- 1단계: `{patterns[i]}`\n  > \"{contents[i]}\"")
                print(f"- 2단계: `{patterns[i+1]}`\n  > \"{contents[i+1]}\"")
                print(f"- 3단계: `{patterns[i+2]}`\n  > \"{contents[i+2]}\"")
                print("\n" + "-"*30 + "\n")
                break # 한 스크립트당 하나만 표시
        else: continue
        break

    # 2. STORY_TELLING 루프 찾기
    print("\n## 사례 2: 스토리텔링 몰입 루프 (Storytelling -> Storytelling -> Metaphor)")
    for name, group in df.groupby('script_id'):
        patterns = group['pattern_id'].tolist()
        contents = group['content'].tolist()
        for i in range(len(patterns)-2):
            if 'STORY_TELLING' in patterns[i] and 'STORY_TELLING' in patterns[i+1] and 'METAPHOR' in patterns[i+2]:
                print(f"**[상담명: {name}]**")
                print(f"- 1단계: `{patterns[i]}`\n  > \"{contents[i]}\"")
                print(f"- 2단계: `{patterns[i+1]}`\n  > \"{contents[i+1]}\"")
                print(f"- 3단계: `{patterns[i+2]}`\n  > \"{contents[i+2]}\"")
                print("\n" + "-"*30 + "\n")
                break
        else: continue
        break

    # 3. TRUISM -> SUGGESTION 체인 찾기
    print("\n## 사례 3: 설득 및 암시 체인 (Truism -> Suggestion -> Action)")
    for name, group in df.groupby('script_id'):
        patterns = group['pattern_id'].tolist()
        contents = group['content'].tolist()
        for i in range(len(patterns)-2):
            if 'TRUISM' in patterns[i] and 'SUGGESTION' in patterns[i+1] and 'ACTION' in patterns[i+2]:
                print(f"**[상담명: {name}]**")
                print(f"- 1단계: `{patterns[i]}`\n  > \"{contents[i]}\"")
                print(f"- 2단계: `{patterns[i+1]}`\n  > \"{contents[i+1]}\"")
                print(f"- 3단계: `{patterns[i+2]}`\n  > \"{contents[i+2]}\"")
                print("\n" + "-"*30 + "\n")
                break
        else: continue
        break

if __name__ == "__main__":
    find_real_examples()
