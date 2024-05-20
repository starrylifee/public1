import pathlib
import random
import google.generativeai as genai
import streamlit as st
import toml

# secrets.toml 파일 경로
secrets_path = pathlib.Path(__file__).parent.parent / ".streamlit" / "secrets.toml"

# secrets.toml 파일 읽기
try:
    with open(secrets_path, "r") as f:
        secrets = toml.load(f)
except FileNotFoundError:
    st.error(f"secrets.toml 파일을 찾을 수 없습니다: {secrets_path}")
    st.stop()
except Exception as e:
    st.error(f"secrets.toml 파일을 읽는 중 오류가 발생했습니다: {e}")
    st.stop()

# 여러 API 키 값 가져오기
api_keys = [
    secrets.get("gemini_api_key1"),
    secrets.get("gemini_api_key2"),
    secrets.get("gemini_api_key3"),
    secrets.get("gemini_api_key4"),
    secrets.get("gemini_api_key5"),
    secrets.get("gemini_api_key6"),
    secrets.get("gemini_api_key7"),
    secrets.get("gemini_api_key8"),
    secrets.get("gemini_api_key9"),
    secrets.get("gemini_api_key10"),
    secrets.get("gemini_api_key11"),
    secrets.get("gemini_api_key12")
]

# 랜덤하게 API 키 선택
selected_api_key = random.choice(api_keys)

# few-shot 프롬프트 구성 함수
def try_generate_content(api_key, prompt_parts):
    # API 키 설정
    genai.configure(api_key=api_key)
    
    # 모델 설정
    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                  generation_config={
                                      "temperature": 0.9,
                                      "top_p": 1,
                                      "top_k": 1,
                                      "max_output_tokens": 2048,
                                  },
                                  safety_settings=[
                                      {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                      {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                      {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                      {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                  ])
    try:
        # 콘텐츠 생성 시도
        response = model.generate_content(prompt_parts)
        return response.text
    except Exception as e:
        # 예외 발생 시 None 반환
        print(f"API 호출 실패: {e}")
        return None

# 스트림릿 앱 인터페이스 구성
st.title("✍️ 글을 어떻게 끝맺으면 좋을까? ✍️")
st.write("""
1. ✏️ 글의 주제를 입력하세요.
2. 📖 글의 성격을 선택하세요.
3. 📝 글의 내용을 입력하세요.
4. 📤 모든 입력을 완료한 후 "글 마무리 전략 생성하기" 버튼을 클릭하세요.
5. 💡 인공지능이 여러분의 입력을 바탕으로 글을 매력적으로 마무리하는 전략을 제안해줍니다.
""")

st.write("📢 이 앱은 창도초등학교 5학년 5반 김민산 학생의 아이디어로 만들어졌습니다. 🎉👏")

# 상태 관리 변수 설정
if 'topic' not in st.session_state:
    st.session_state['topic'] = ""
if 'style' not in st.session_state:
    st.session_state['style'] = "설명하는 글"
if 'intro' not in st.session_state:
    st.session_state['intro'] = ""
if 'middle1' not in st.session_state:
    st.session_state['middle1'] = ""
if 'middle2' not in st.session_state:
    st.session_state['middle2'] = ""
if 'middle3' not in st.session_state:
    st.session_state['middle3'] = ""

# 입력 필드
topic = st.text_input("1. 글의 주제", value=st.session_state['topic'])
style = st.selectbox("2. 글의 성격", ["설명하는 글", "주장하는 글"], index=["설명하는 글", "주장하는 글"].index(st.session_state['style']))
intro = st.text_area("3. 글의 처음 내용", value=st.session_state['intro'])
middle1 = st.text_area("4. 글의 중간 내용 - 1", value=st.session_state['middle1'])
middle2 = st.text_area("5. 글의 중간 내용 - 2", value=st.session_state['middle2'])
middle3 = st.text_area("6. 글의 중간 내용 - 3", value=st.session_state['middle3'])

# 입력 값 검증 및 인공지능 호출
if st.button("글 마무리 전략 생성하기"):
    if not all([topic, style, intro, middle1, middle2, middle3]):
        st.warning("모든 입력을 작성해주세요!")
    else:
        # 입력값을 상태 변수에 저장
        st.session_state['topic'] = topic
        st.session_state['style'] = style
        st.session_state['intro'] = intro
        st.session_state['middle1'] = middle1
        st.session_state['middle2'] = middle2
        st.session_state['middle3'] = middle3

        # 프롬프트 구성
        prompt_parts = [
            "다음은 주어진 주제와 글의 성격, 내용을 바탕으로 작성된 글입니다. 이 글을 매력적으로 마무리할 수 있는 전략을 제안해주세요.\n\n",
            f"1. 글의 주제: {topic}",
            f"2. 글의 성격: {style}",
            f"3. 글의 처음 내용: {intro}",
            f"4. 글의 중간 내용 - 1: {middle1}",
            f"5. 글의 중간 내용 - 2: {middle2}",
            f"6. 글의 중간 내용 - 3: {middle3}",
            "\n글을 매력적으로 마무리할 수 있는 전략을 제안해주세요."
        ]

        # API 호출 시도
        response_text = try_generate_content(selected_api_key, prompt_parts)
        
        # 첫 번째 API 키 실패 시, 다른 API 키로 재시도
        if response_text is None:
            for api_key in api_keys:
                if api_key != selected_api_key:
                    response_text = try_generate_content(api_key, prompt_parts)
                    if response_text is not None:
                        break
        
        # 결과 출력
        if response_text is not None:
            st.success("글 마무리 전략 생성 완료!")
            st.text_area("생성된 마무리 전략:", value=response_text, height=300)
            st.download_button(label="마무리 전략 다운로드", data=response_text, file_name="ending_strategy.txt", mime="text/plain")
            st.write("인공지능이 생성한 전략은 꼭 본인이 확인해야 합니다. 생성된 전략을 검토하고, 필요한 경우에만 수정하세요.")
        else:
            st.error("API 호출에 실패했습니다. 나중에 다시 시도해주세요.")

# 세션 초기화 버튼
if st.button("다시 시작하기"):
    st.session_state['topic'] = ""
    st.session_state['style'] = "설명하는 글"
    st.session_state['intro'] = ""
    st.session_state['middle1'] = ""
    st.session_state['middle2'] = ""
    st.session_state['middle3'] = ""
    st.experimental_rerun()
