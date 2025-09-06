import streamlit as st

st.set_page_config(page_title="Simple Chat", page_icon="💬")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("💬 간단한 챗봇")

# 이전 대화 출력
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# 사용자 입력
user_input = st.chat_input("메시지를 입력하세요...")

if user_input:
    # 사용자 메시지 출력
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 응답 생성
    if user_input.strip() == "안녕":
        reply = "뭐 임마"
    else:
        reply = "무슨 말인지 모르겠어요."

    # 봇 응답 출력
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
