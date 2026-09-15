import streamlit as st
from groq import Groq
from langdetect import detect

# 페이지 설정
st.set_page_config(page_title="HANEOL AI", page_icon="🧭", layout="wide")

# CSS 스타일 정의
st.markdown("""
<style>
    .stApp { background-color: #f7f9fc; }
    .main-title { font-size: 2.2rem; font-weight: 800; color: #1e293b; text-align: center; }
    .sub-title { font-size: 0.95rem; color: #64748b; text-align: center; margin-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)

# Groq 클라이언트 초기화 (하드코딩 방식)
client = Groq(api_key="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")

# 헤더
st.markdown("<h1 class='main-title'>🧭 HANEOL AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>본질과 맥락을 가로지르는 입체적 통찰</p>", unsafe_allow_html=True)

# 메시지 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 메시지 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 사용자 입력 처리
if user_input := st.chat_input("질문이나 고민을 입력해 보세요..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            
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
