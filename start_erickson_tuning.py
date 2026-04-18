import google.generativeai as genai
import os
import time

# 🗝️ API 설정
# 환경 변수 혹은 직접 입력을 사용하세요.
API_KEY = os.environ.get("GOOGLE_API_KEY", "YOUR_API_KEY_HERE")
genai.configure(api_key=API_KEY)

def start_tuning_job(source_csv_path, model_name="gemini-1.5-flash"):
    """
    Google AI Studio 서버로 파인튜닝 요청을 보냅니다.
    """
    if not os.path.exists(source_csv_path):
        print(f"❌ 파일을 찾을 수 없습니다: {source_csv_path}")
        return

    print(f"🚀 파인튜닝 작업 시작...")
    print(f" - 데이터셋: {os.path.basename(source_csv_path)}")
    print(f" - 베이스 모델: {model_name}")

    try:
        # 1. 튜닝 작업 생성
        # display_name은 AI Studio 대시보드에서 보일 이름입니다.
        operation = genai.create_tuned_model(
            source_model=f"models/{model_name}",
            training_data=source_csv_path, # CSV 파일 경로를 직접 넣을 수 있습니다.
            id=f"erickson-dna-{int(time.time())}",
            display_name="Milton Erickson Style DNA (Essential 1500)",
            epoch_count=3,
            batch_size=16,
            learning_rate=0.001,
        )

        print("-" * 50)
        print(f"✅ 튜닝 요청이 성공적으로 전송되었습니다!")
        print(f"작업 ID: {operation.name}")
        print("-" * 50)
        
        print("\n⏳ 인내심이 필요합니다. 학습이 완료될 때까지 기다려야 합니다.")
        print("AI Studio 대시보드(https://aistudio.google.com/app/tuned_models)에서")
        print("진행 상황을 실시간으로 확인하실 수 있습니다.")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    # 방금 생성한 고품질 1500개 데이터셋 경로
    dataset_path = r"C:\Users\magic\Downloads\erickson_data\erickson_tuning_essential_1500.csv"
    
    # 모델 선택: 'gemini-1.5-flash' 혹은 'gemini-1.0-pro-001' 등 지원 모델 확인 필요
    start_tuning_job(dataset_path, model_name="gemini-1.5-flash")
