from openai import OpenAI
import streamlit as st
import time
import random
import pathlib
import toml

# Streamlit의 기본 메뉴와 푸터 숨기기
hide_github_icon = """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK{ display: none; }
    #MainMenu{ visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    </style>
"""

st.markdown(hide_github_icon, unsafe_allow_html=True)

def load_css():
    css = """
    <style>
        body, .stApp, .stChatFloatingInputContainer {
            background-color: #F0F8FF !important; /* 배경을 좀 더 밝은 색으로 변경 */
            font-family: 'Arial', sans-serif; /* 글꼴 스타일을 설정 */
        }
        .stChatInputContainer {
            background-color: #E0F7FA !important; /* 입력 필드의 배경색도 변경 */
        }
        textarea {
            background-color: #FFFFFF !important; /* 실제 입력 필드의 배경색도 흰색으로 변경 */
            color: #333333 !important; /* 글자색을 검정색으로 변경 */
        }
        .stButton>button {
            background-color: #007BFF !important; /* 버튼 색상 변경 */
            color: white !important; /* 버튼 텍스트 색상 */
        }
        .stButton>button:hover {
            background-color: #0056b3 !important; /* 버튼 호버 색상 */
        }
        .stChatMessage {
            border-radius: 10px; /* 메시지의 모서리를 둥글게 */
            padding: 10px; /* 메시지 안쪽 여백 설정 */
            margin-bottom: 10px; /* 메시지 간격 설정 */
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def main():
    load_css()  # 배경색 스타일 로드

    # 초기화 조건 수정
    if "initialized" not in st.session_state:
        st.session_state.thread_id = ""  # 스레드 ID 초기화
        st.session_state.messages = [{"role": "assistant", "content": "안녕하세요! 저는 서울특별시교육청의 학적업무 도움자료를 바탕으로 개발된 교육 지원 챗봇입니다. 어떤 정보를 도와드릴까요?"}]  # 초기 메시지 설정
        st.session_state.initialized = True

    # secrets.toml 파일 경로
    secrets_path = pathlib.Path(__file__).parent.parent / ".streamlit/secrets.toml"

    # secrets.toml 파일 읽기
    with open(secrets_path, "r", encoding="utf-8") as f:
        secrets = toml.load(f)

    # secrets.toml 파일에서 여러 API 키 값 가져오기
    api_keys = [
        secrets.get("api_key1"),
        secrets.get("api_key2"),
        secrets.get("api_key3"),
        secrets.get("api_key4"),
        secrets.get("api_key5"),
        secrets.get("api_key6"),
        secrets.get("api_key7"),
        secrets.get("api_key8"),
        secrets.get("api_key9"),
        secrets.get("api_key10"),
        secrets.get("api_key11"),
        secrets.get("api_key12")
    ]

    # 유효한 API 키 필터링
    api_keys = [key for key in api_keys if key is not None]

    # 랜덤하게 API 키를 선택하여 OpenAI 클라이언트 초기화
    selected_api_key = random.choice(api_keys)
    client = OpenAI(api_key=selected_api_key)

    # 스레드 자동 생성 및 관리
    if "thread_id" not in st.session_state or not st.session_state.thread_id:
        try:
            thread = client.beta.threads.create()
            st.session_state.thread_id = thread.id  # 스레드 ID를 session_state에 저장
            st.sidebar.success("자동으로 대화가 시작되었습니다!")
        except Exception as e:
            st.sidebar.error("자동 대화 시작에 실패했습니다. 다시 시도해주세요.")
            st.sidebar.error(str(e))

    with st.sidebar:
        st.divider()
        if "show_examples" not in st.session_state:
            st.session_state.show_examples = True

        if st.session_state.show_examples:
            st.subheader("질문 예시")
            st.info("입학 절차에 대해 알려줘")
            st.info("출석 관리 방법을 알고 싶어")
            st.info("생활기록부 기재 요령이 궁금해")

    # 스레드 ID 입력란을 자동으로 업데이트
    thread_id = st.session_state.thread_id

    st.title("학적업무 도움 챗봇")
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        if not thread_id:
            st.error("대화 시작에 문제가 발생했습니다. 페이지를 새로고침 해주세요.")
            st.stop()

        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # 스피너 추가
        with st.spinner('응답을 생성하는 중입니다...'):
            response = client.beta.threads.messages.create(
                thread_id,
                role="user",
                content=prompt,
            )

            run = client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=secrets["assistant_api_key2"]
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
