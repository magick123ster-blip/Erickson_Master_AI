import streamlit as st
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI
import os
import sys

# 1. Setup Environment (Use relative paths)
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'erickson_vector_db')

st.set_page_config(page_title="Erickson Portable Training Center", page_icon="🎓", layout="wide")

# 2. Initialize Database (Portable)
@st.cache_resource
def get_collection():
    if not os.path.exists(db_path):
        st.error(f"데이터베이스를 찾을 수 없습니다: {db_path}")
        return None
    client = chromadb.PersistentClient(path=db_path)
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    return client.get_collection(name="erickson_strategies", embedding_function=emb_fn)

# 3. Master Statistical DNA
MASTER_DNA = """
[📊 에릭슨 전략 지능]
- 데이터: 1,805개 전략 체인 기반
- 훈련 모드: 실전 시퀀스 코칭 시스템
"""

# 4. State & Sidebar
if "messages" not in st.session_state:
    st.session_state.messages = []
if "training_step" not in st.session_state:
    st.session_state.training_step = 0

st.sidebar.title("🎓 Erickson Academy")
st.sidebar.subheader("🎯 훈련 테마 선택")
training_themes = ["라포 및 동조", "저항 활용", "패턴 중단", "은유적 암시", "역설적 개입", "이중 구속", "혼란 기법", "미래 투사"]
selected_theme = st.sidebar.selectbox("연습할 전략", training_themes)

if st.sidebar.button("🚀 새 훈련 시작"):
    st.session_state.messages = []
    st.session_state.training_step = 0
    st.session_state.pending_trigger = f"나는 지금 '{selected_theme}' 전략을 훈련하고 싶어. 시나리오를 주고 1단계 미션을 줘."

st.sidebar.markdown("---")
api_key = st.sidebar.text_input("API Key 입력", type="password")
model_name = st.sidebar.selectbox("모델 선택", ["gemini-3.1-pro-preview", "gemini-3-flash-preview", "gemma-4-31b-it"])

# 5. Trainer Logic
TRAINER_PROMPT = f"당신은 에릭슨 전문 훈련관입니다. {MASTER_DNA}\n시나리오를 주도하고 단계별로 피드백을 주며 훈련을 이끄십시오."

# 6. UI
st.title("🎓 Erickson Professional Trainer (Portable)")
st.markdown("---")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("에릭슨 스타일 문장 입력...")
if "pending_trigger" in st.session_state:
    prompt = st.session_state.pending_trigger
    del st.session_state.pending_trigger

if prompt:
    if "나는 지금" not in prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

    collection = get_collection()
    context = ""
    if collection:
        results = collection.query(query_texts=[prompt], n_results=3)
        for doc in results['documents'][0]: context += f"\n[DNA 사례]\n{doc}\n"
    
    if api_key:
        client = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/", api_key=api_key)
        with st.chat_message("assistant"):
            full_response = ""
            resp = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "system", "content": TRAINER_PROMPT + f"\n[데이터]\n{context}"}, {"role": "user", "content": prompt}],
                stream=True
            )
            placeholder = st.empty()
            for chunk in resp:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)
            st.session_state.training_step += 1
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.rerun()
