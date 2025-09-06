import os
st.markdown(m["content"])


user_input = st.chat_input("메시지를 입력하세요…")


if user_input:
st.session_state.messages.append({"role": "user", "content": user_input})
with st.chat_message("user"):
st.markdown(user_input)


with st.chat_message("assistant"):
if backend == "OpenAI-compatible":
if not api_key:
st.error("API Key가 필요합니다.")
else:
placeholder = st.empty()
acc = ""
for chunk in openai_chat_completion(st.session_state.messages):
if isinstance(chunk, dict) and "__complete__" in chunk:
acc = chunk["__complete__"]
break
else:
acc += chunk
placeholder.markdown(acc)
st.session_state.messages.append({"role": "assistant", "content": acc})
else:
if not api_key:
st.error("HuggingFace API Token이 필요합니다.")
else:
reply = hf_text_completion(st.session_state.messages)
st.markdown(reply)
st.session_state.messages.append({"role": "assistant", "content": reply})


###############################
# ---- UI: Image Generation ----
###############################
else:
st.title("🎨 Image Generation")
st.caption("프롬프트로 이미지를 생성합니다 (OpenAI-호환 API 사용)")


if backend != "OpenAI-compatible":
st.info("이미지 생성은 현재 OpenAI-호환 백엔드에서만 동작하도록 구현되어 있습니다.")


prompt = st.text_area("프롬프트 입력", placeholder="예: a photorealistic macro shot of a dewdrop on a leaf")
size = st.selectbox("이미지 크기", ["512x512", "768x768", "1024x1024"], index=2)
gen = st.button("이미지 생성")


if gen:
if backend != "OpenAI-compatible":
st.error("이미지 생성을 사용하려면 'OpenAI-compatible' 백엔드를 선택하세요.")
elif not api_key:
st.error("API Key가 필요합니다.")
elif not prompt.strip():
st.error("프롬프트를 입력하세요.")
else:
with st.spinner("생성 중…"):
try:
img_bytes = openai_image_generation(prompt, size=size)
except Exception as e:
st.error(f"이미지 생성 실패: {e}")
else:
st.image(img_bytes, caption=prompt)
st.download_button(
"이미지 다운로드",
data=img_bytes,
file_name="genai_image.png",
mime="image/png",
)


############################
# ---- Footer / Tips ----
############################
st.sidebar.markdown("""
**Tips**
- OpenAI-compatible 서버 예시: OpenAI, Together, Groq, Mistral, Perplexity 등에서 제공하는 호환 엔드포인트.
- 회사/학교 프록시 뒤에 있다면 `Base URL`을 해당 게이트웨이로 변경하세요.
- `st.secrets`에 API 키를 넣고 `os.getenv` 대신 사용해도 됩니다.
""")
