import streamlit as st

st.set_page_config(page_title="Simple Chat", page_icon="💬")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title(" 싸가지 없는 챗봇")

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

    # 입력을 소문자 + 공백 제거 처리
    cleaned_input = user_input.strip().lower()

    # 유연한 단어 인식
    if "안녕" in cleaned_input:
        reply = "뭐 임마"
    elif "느금마" in cleaned_input:
        reply = "니도 없잖아 임마"
    else:
        reply = "무슨 말인지 모르겠어요."

    # 챗봇 응답 출력
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
