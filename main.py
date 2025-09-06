import streamlit as st
import requests
import json
import os

st.set_page_config(page_title="My GenAI App", page_icon="🤖")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

st.title("🤖 Streamlit Generative AI Chat")

# 이전 대화 보여주기
for m in st.session_state.messages:
    if m["role"] == "system":
        continue
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# 사용자 입력
user_input = st.chat_input("메시지를 입력하세요...")

if user_input:
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # OpenAI API 호출
    api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
    if not api_key:
        with st.chat_message("assistant"):
            st.error("API Key가 없습니다. 환경변수 OPENAI_API_KEY를 설정하세요.")
    else:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": "gpt-4o-mini",  # 원하면 다른 모델명으로 교체 가능
            "messages": st.session_state.messages,
            "max_tokens": 500
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"]
            with st.chat_message("assistant"):
                st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        else:
            with st.chat_message("assistant"):
                st.error(f"API 오류: {response.text}")
