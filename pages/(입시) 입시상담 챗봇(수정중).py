from openai import OpenAI
import streamlit as st
import time

# 업데이트된 Assistant ID
assistant_id = "asst_QVROlrgiLyvFZWQmB6WXCfxX"

st.title("법률제작 보조 챗봇")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key:", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")
else:
    # API 키가 입력되면 클라이언트와 스레드를 초기화합니다.
    client = OpenAI(api_key=openai_api_key)
    # 사용자 세션당 한 번만 스레드를 생성합니다.
    if "thread_id" not in st.session_state:
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id  # 생성된 스레드 ID 저장

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요, 저는 입시 상담 봇입니다. 어떻게 도와드릴까요?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    thread_id = st.session_state.thread_id
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = client.beta.threads.messages.create(
        thread_id,
        role="user",
        content=prompt,
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    run_id = run.id

    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )
        if run.status == "completed":
            break
        else:
            time.sleep(2)

    thread_messages = client.beta.threads.messages.list(thread_id)

    msg = thread_messages.data[0].content[0].text.value
    
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
