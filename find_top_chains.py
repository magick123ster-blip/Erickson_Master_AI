import pandas as pd
import os

DATA_DIR = r'C:\Users\magic\Downloads\erickson_data'
MAP_CSV = os.path.join(DATA_DIR, 'complete_strategic_map.csv')
DIST_CSV = os.path.join(DATA_DIR, 'full_stationary_distribution.csv')

def find_chains():
    df = pd.read_csv(MAP_CSV)
    pi = pd.read_csv(DIST_CSV)
    
    # 1. Theoretical Most Probable Chains (Greedy)
    top_starts = pi.head(15)['pattern_id'].tolist()
    
    print("### [상위 15개 핵심 전략 경로 (3단계 연결)]\n")
    print("이 경로는 세션에서 가장 중요한 발화 패턴에서 시작하여, 에릭슨이 가장 높은 확률로 선택하는 다음 단계들을 추적한 결과입니다.\n")

    for i, start in enumerate(top_starts):
        chain = [start]
        curr = start
        total_prob = 1.0
        
        for _ in range(3):
            next_steps = df[df['Current'] == curr].sort_values('Probability', ascending=False)
            if not next_steps.empty:
                best_next = next_steps.iloc[0]
                curr = best_next['Next']
                prob = best_next['Probability']
                chain.append(curr)
                total_prob *= prob
            else:
                break
        
        path_str = " -> ".join([f"`{p}`" for p in chain])
        print(f"{i+1}. **시작: {start}**")
        print(f"   - 경로: {path_str}")
        print(f"   - 경로 신뢰도 (누적 확률): {total_prob:.4f}\n")

if __name__ == "__main__":
    find_chains()
