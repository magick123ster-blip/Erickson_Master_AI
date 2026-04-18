__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI
import os
import sys
from datetime import datetime

# 1. Setup Environment
sys.path.append(os.path.expanduser("~/AppData/Roaming/Python/Python313/site-packages"))

st.set_page_config(page_title="Erickson Master AI (Deep Logic Edition)", page_icon="🧠", layout="wide")

# 2. Initialize Database (Cached)
@st.cache_resource
def get_collection():
    db_path = 'erickson_vector_db'
    if not os.path.exists(db_path):
        return None
    client = chromadb.PersistentClient(path=db_path)
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    return client.get_collection(name="erickson_strategies", embedding_function=emb_fn)

# 3. Master Statistical DNA
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

# Save history
if "messages" not in st.session_state:
    st.session_state.messages = []

def get_chat_text():
    chat_text = f"Erickson AI Session Log\n"
    for msg in st.session_state.messages:
        chat_text += f"[{msg['role']}]: {msg['content']}\n\n"
    return chat_text

st.sidebar.markdown("---")
if st.session_state.messages:
    st.sidebar.download_button(label="💾 세션 기록 저장 (.txt)", data=get_chat_text(), file_name="Erickson_Log.txt")

# 5. Master Prompts (Deep Logic Enhanced)
INFERENCE_PROTOCOL = "절대 간결하게 답변하지 마십시오. 최소 3단계 이상의 심층 추론(Step-by-step Reasoning)을 거친 뒤, 풍성하고 상세한 결과물을 출력하십시오."

CONSULTATION_PROMPT = f"당신은 '밀턴 에릭슨'입니다. {INFERENCE_PROTOCOL}\n{MASTER_DNA}\n은유와 비유를 사용하여 따뜻하게 상담하십시오."

LEARNING_PROMPT = f"당신은 '에릭슨 전략 아키텍트'입니다. {INFERENCE_PROTOCOL}\n{MASTER_DNA}\n전략적 시퀀스를 학술적으로 해부하여 가르치십시오."

# Enhanced Transformer Prompt with Content Completeness
TRANSFORM_PROMPT = f"""
당신은 '에릭슨 스타일 딥-트랜스포머(Deep Transformer)'입니다. {MASTER_DNA}
[핵심 임무] 사용자의 글을 에릭슨의 문체로 재작성하되, 원문의 내용을 '절대로 요약하지 마십시오'.

[심층 변환 수칙]
1. 원문 전수 보존: 원문에 포함된 모든 정보, 수치, 의도를 하나도 빠짐없이 결과물에 담아내십시오. 오히려 에릭슨 특유의 부연 설명을 더해 원문보다 '더 길고 풍성하게' 만드십시오.
2. 3단계 심층 추론: 변환 전, 각 문장의 심리적 의도를 먼저 분석하고, 어떤 에릭슨 기법(수동태 2.8배, Truism 등)을 적용할지 깊이 추론한 뒤 작성하십시오.
3. 은유적 확장: 딱딱한 정보성 문장을 만날 때마다, 그것을 에릭슨식의 따뜻한 비유와 우회적인 표현으로 확장하십시오.
4. 기술 통계 리포트: 변환 후에는 사용된 모든 기법의 빈도와 그 전략적 이유를 상세히 서술하십시오.

어투: 매우 지적이고 마법 같은 문체로 변환하십시오. 요약은 실패로 간주합니다.
"""

TRAINER_PROMPT = f"당신은 '에릭슨 전략 개인 훈련관'입니다. {INFERENCE_PROTOCOL} {MASTER_DNA}\n시나리오를 주도하고 단계별로 피드백을 주며 훈련을 이끄십시오."

# 6. Main UI
st.title(f"🧠 Erickson Master AI ({app_mode})")
st.markdown("---")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

input_label = "변환할 컨텐츠를 입력하세요..." if "변환" in app_mode else "메시지를 입력하세요..."
if prompt := st.chat_input(input_label):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    collection = get_collection()
    retrieved_context = "관련 DNA 사례 검색 중..."
    if collection:
        results = collection.query(query_texts=[prompt], n_results=5)
        if results and results['documents'] and len(results['documents'][0]) > 0:
            retrieved_context = ""
            for i in range(len(results['documents'][0])):
                doc = results['documents'][0][i]
                meta = results['metadatas'][0][i]
                retrieved_context += f"\n--- [DNA 사례 #{i+1} ({meta.get('type')})] ---\n{doc}\n"
    
    if not api_key:
        st.warning(f"{provider} API Key 필요")
    else:
        client = OpenAI(base_url=base_url, api_key=api_key)
        if "상담" in app_mode: mode_instruction = CONSULTATION_PROMPT
        elif "학습" in app_mode: mode_instruction = LEARNING_PROMPT
        elif "변환" in app_mode: mode_instruction = TRANSFORM_PROMPT
        else: mode_instruction = TRAINER_PROMPT
        
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
                    temperature=0.75,
                    max_tokens=4000,
                    stream=True
                )
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                
                with st.expander("📚 [클릭] 분석 및 변환의 근거 데이터 보기"):
                    st.info(MASTER_DNA)
                    st.text(retrieved_context)
                    
            except Exception as e:
                st.error(f"오류: {e}")
                
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.rerun()
