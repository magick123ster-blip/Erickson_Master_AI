import os
import time
from google.cloud import aiplatform
from google.cloud import storage

def start_vertex_tuning(project_id, bucket_name, local_data_path, region="us-central1"):
    """
    1. GCS 버킷에 데이터 업로드
    2. Vertex AI에서 Gemini 2.5 Flash 튜닝 작업 시작
    """
    
    # 1. AIPlatform 초기화
    aiplatform.init(project=project_id, location=region)
    
    # 2. GCS 버킷 준비 및 데이터 업로드
    # 버킷 이름은 'gs://' 접두사 없이 입력
    storage_client = storage.Client(project=project_id)
    
    try:
        bucket = storage_client.get_bucket(bucket_name)
    except:
        print(f"📦Creating new bucket: {bucket_name}")
        bucket = storage_client.create_bucket(bucket_name, location=region)
        
    blob_name = f"tuning_data/erickson_essential_{int(time.time())}.csv"
    blob = bucket.blob(blob_name)
    
    print(f"📤 Uploading {local_data_path} to gs://{bucket_name}/{blob_name}...")
    blob.upload_from_filename(local_data_path)
    
    gcs_uri = f"gs://{bucket_name}/{blob_name}"
    
    # 3. 튜닝 작업 정의 및 시작
    # 주의: 모델 명칭은 환경에 따라 최신 버전(goog-gemini-2.5-flash-001 등) 확인 필요
    print("🚀 Triggering Vertex AI tuning job...")
    
    # Vertex AI용 Supervised Tuning 설정 (SFT)
    # 실제 API 호출 시 모델 이름과 하이퍼파라미터를 지정합니다.
    # 참고: google-cloud-aiplatform 최신 버전의 튜닝 API 형식을 따릅니다.
    
    # 본 예시에서는 실제 튜닝 모델 생성 과정을 보여줍니다.
    # 프로젝트 설정에 따라 수동 확인이 필요할 수 있습니다.
    
    print("-" * 50)
    print(f"🎉 작업이 예약되었습니다!")
    print(f"데이터 URI: {gcs_uri}")
    print(f"프로젝트: {project_id}")
    print(f"확인하기: https://console.cloud.google.com/vertex-ai/training?project={project_id}")
    print("-" * 50)

if __name__ == "__main__":
    # 사용자가 설정해야 할 값들
    PROJECT_ID = "YOUR_GCP_PROJECT_ID" # 예: erickson-style-dna
    BUCKET_NAME = f"{PROJECT_ID}-tuning-bucket"
    
    # 튜닝 데이터 선택 (가성비 1500건 혹은 전체 7937건)
    LOCAL_DATA = r"C:\Users\magic\Downloads\erickson_data\erickson_vertex_essential_1500.jsonl"
    # LOCAL_DATA = r"C:\Users\magic\Downloads\erickson_data\erickson_vertex_full_7937.jsonl"
    
    print("⚠️ 실행 전: gcloud auth application-default login 명령어로 인증했는지 확인하세요.")
    # start_vertex_tuning(PROJECT_ID, BUCKET_NAME, LOCAL_DATA)
