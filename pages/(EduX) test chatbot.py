from openai import OpenAI
import streamlit as st
import time

def load_css():
    css = """
    <style>
        body, .stApp, .stChatFloatingInputContainer {
            background-color: #E1BEE7 !important; /* Light lavender color */
        }
        .stChatInputContainer {
            background-color: #E1BEE7 !important; /* Light lavender color */
        }
        textarea {
            background-color: #FFFFFF !important; /* White background for the input field */
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def main():
    load_css()  # Load background style

    if "initialized" not in st.session_state:
        st.session_state.thread_id = ""
        st.session_state.messages = [{"role": "assistant", "content": "안녕하세요, 저는 AI융합수교멘토운영안내 보조 챗봇입니다. 먼저 왼쪽의 '대화 시작'버튼을 눌러주세요. 무엇을 도와드릴까요?"}]
        st.session_state.initialized = True

    with st.sidebar:
        assistant_id = st.text_input("Assistant ID를 입력하세요", type='password')
        api_key = st.text_input("Openai API key를 입력하세요", type='password')
        thread_btn = st.button("대화 시작")

    client = None
    try:
        client = OpenAI(api_key=api_key)
    except Exception as e:
        st.error("API 키 오류: " + str(e))
        st.stop()

    if thread_btn:
        try:
            thread = client.beta.threads.create()
            st.session_state.thread_id = thread.id
            st.success("대화가 시작되었습니다!")
        except Exception as e:
            st.error("대화 시작에 실패했습니다. 다시 시도해주세요.")
            st.error(str(e))

    st.divider()

    thread_id = st.session_state.thread_id
    st.title("AI융합수교멘토운영안내 보조 챗봇")
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        if not thread_id:
            st.error("왼쪽의 대화시작 버튼을 눌러주세요.")
            st.stop()

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

if __name__ == "__main__":
    main()
