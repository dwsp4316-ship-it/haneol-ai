import streamlit as st
from groq import Groq
from langdetect import detect

# 1. 페이지 및 레이아웃 설정
st.set_page_config(page_title="HANEOL AI", page_icon="🧭", layout="wide")

# 2. 배경 디자인 및 CSS 스타일 복구
st.markdown("""
<style>
    /* 배경 그리드 패턴 복구 */
    .stApp {
        background-color: #f8fafc;
        background-image: 
            linear-gradient(to right, rgba(226, 232, 240, 0.6) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(226, 232, 240, 0.6) 1px, transparent 1px);
        background-size: 30px 30px;
    }
    
    /* 타이틀 및 UI 스타일링 */
    .main-title { font-size: 2.3rem; font-weight: 800; color: #0f172a; text-align: center; }
    .sub-title { font-size: 0.95rem; color: #475569; text-align: center; margin-bottom: 2rem; }
    
    /* 채팅 메시지 카드 스타일링 */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# 3. Groq 클라이언트 초기화
client = Groq(api_key="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")

# 4. 헤더 UI
st.markdown("<h1 class='main-title'>🧭 HANEOL AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>본질과 맥락을 가로지르는 입체적 통찰</p>", unsafe_allow_html=True)

# 5. 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 6. 사용자 입력 및 AI 응답 처리
if user_input := st.chat_input("질문이나 고민을 입력해 보세요..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            try:
                lang = detect(user_input)
            except:
                lang = "ko"

            system_instruction = (
                "You are 'HANEOL AI', an insightful, empathetic, and multi-perspective AI assistant. "
                "Analyze the core essence and context of the user's inquiry, providing clear and structured answers. "
            )
            if lang == "ko":
                system_instruction += "답변은 친절하고 명확한 한국어로 작성해 주세요."
            else:
                system_instruction += f"Respond appropriately in the detected language ({lang})."

            api_messages = [{"role": "system", "content": system_instruction}]
            for m in st.session_state.messages:
                api_messages.append({"role": m["role"], "content": m["content"]})
            
            stream = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=api_messages,
                stream=True,
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"API 호출 실패! 에러: {e}")
