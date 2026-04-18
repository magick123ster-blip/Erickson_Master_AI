try:
    # 클라우드(리눅스) 환경에서 SQLite 버전 문제를 해결하기 위한 코드
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    # 로컬(윈도우) 환경에서는 위 코드가 실패하며, 자연스럽게 기본 sqlite3를 사용합니다.
    pass

import streamlit as st
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI
import os
from datetime import datetime

# 1. Page Config
st.set_page_config(page_title="Erickson Master AI", page_icon="🧠", layout="wide")

# 2. Initialize Database (Cached)
@st.cache_resource
def get_collection():
    db_path = 'erickson_vector_db'
    if not os.path.exists(db_path):
        st.error(f"데이터베이스 경로를 찾을 수 없습니다: {db_path}")
        return None
    try:
        client = chromadb.PersistentClient(path=db_path)
        emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        return client.get_collection(name="erickson_strategies", embedding_function=emb_fn)
    except Exception as e:
        st.error(f"데이터베이스 로드 오류: {e}")
        return None

# 3. Master DNA
MASTER_DNA = """
[📊 에릭슨 전략 지능]
- 자원: 1,805개 전략 체인, 6,486개 시퀀스
- 수치: PACE->SUGG(42%), TRUISM->IMPL(45%), 수동태 2.8배
"""

# 4. Sidebar
st.sidebar.title("🎮 실행 모드")
app_mode = st.sidebar.radio("모드 선택", ["상담 모드 (Persona)", "학습 모드 (Architect)", "변환 모드 (Transformer)", "훈련 모드 (Trainer)"])
st.sidebar.markdown("---")
st.sidebar.title("⚙️ 모델 설정")
provider = st.sidebar.radio("서비스", ["Google AI Studio", "NVIDIA"])
next_gen_models = ["gemini-3.1-pro-preview", "gemini-3-flash-preview", "gemini-3.1-flash-lite-preview", "gemma-4-31b-it"]
if provider == "NVIDIA":
    api_key = st.sidebar.text_input("NVIDIA API Key", type="password")
    model_options = [f"google/{m}" if "gemma" in m else m for m in next_gen_models]
    base_url = "https://integrate.api.nvidia.com/v1"
else:
    api_key = st.sidebar.text_input("Google API Key", type="password")
    model_options = next_gen_models
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
model_name = st.sidebar.selectbox("모델", model_options)

if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Master Prompts
INFERENCE_PROTOCOL = "최소 3단계 이상의 심층 추론을 거친 뒤 상세히 답변하십시오."
CONSULTATION_PROMPT = f"당신은 '밀턴 에릭슨'입니다. {INFERENCE_PROTOCOL}\n{MASTER_DNA}"
LEARNING_PROMPT = f"당신은 '에릭슨 전략 아키텍트'입니다. {INFERENCE_PROTOCOL}\n{MASTER_DNA}"
TRANSFORM_PROMPT = f"당신은 '에릭슨 스타일 트랜스포머'입니다. 요약 금지, 원문보다 풍성하게 변환하십시오.\n{MASTER_DNA}"
TRAINER_PROMPT = f"당신은 '에릭슨 전략 개인 훈련관'입니다. 시나리오 기반 실전 훈련을 이끄십시오.\n{MASTER_DNA}"

# 6. Main UI
st.title(f"🧠 Erickson Master AI ({app_mode})")
st.markdown("---")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("메시지를 입력하세요..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    collection = get_collection()
    retrieved_context = ""
    if collection:
        results = collection.query(query_texts=[prompt], n_results=5)
        if results and results['documents']:
            for i in range(len(results['documents'][0])):
                retrieved_context += f"\n[DNA 사례 #{i+1}]\n{results['documents'][0][i]}\n"
    
    if api_key:
        client = OpenAI(base_url=base_url, api_key=api_key)
        mode_instruction = CONSULTATION_PROMPT
        if "학습" in app_mode: mode_instruction = LEARNING_PROMPT
        elif "변환" in app_mode: mode_instruction = TRANSFORM_PROMPT
        elif "훈련" in app_mode: mode_instruction = TRAINER_PROMPT
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": mode_instruction + f"\n\n[참조 데이터]\n{retrieved_context}"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=4000,
                    stream=True
                )
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"오류: {e}")
    else:
        st.warning("사이드바에 API Key를 입력해 주세요.")
