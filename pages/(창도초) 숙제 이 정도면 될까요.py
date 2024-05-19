import pathlib
import textwrap
import google.generativeai as genai
import streamlit as st
import toml
import random

# secrets.toml 파일 경로
secrets_path = pathlib.Path(__file__).parent.parent / ".streamlit/secrets.toml"

# secrets.toml 파일 읽기
with open(secrets_path, "r") as f:
    secrets = toml.load(f)

# secrets.toml 파일에서 여러 API 키 값 가져오기
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

# 랜덤하게 API 키를 선택하여 OpenAI 클라이언트 초기화
selected_api_key = random.choice(api_keys)

# few-shot 프롬프트 구성 함수
def try_generate_content(api_key, prompt_parts):
    # API 키를 설정
    genai.configure(api_key=api_key)
    
    # 설정된 모델 변경
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
        # 예외 발생시 None 반환
        print(f"API 호출 실패: {e}")
        return None

# 스트림릿 앱 인터페이스 구성
st.title("📚 숙제 이 정도면 될까요? 📚")
st.write("""
1. 📝 선생님이 내주신 과제를 입력하세요.
2. 📝 본인이 작성한 글을 입력하세요.
3. 📤 모든 입력을 완료한 후 "개선 사항 생성하기" 버튼을 클릭하세요.
4. 💬 인공지능이 여러분의 입력을 바탕으로 더 조사해야 할 점과 더 적어야 할 점을 제안해줍니다.
5. 📥 결과를 다운로드하거나, 제안을 수정하여 사용할 수 있습니다.
""")

st.write("📢 이 앱은 창도초등학교 5학년 5반 장유진 학생의 아이디어로 만들어졌습니다. 🎉👏")

# 입력 필드
assignment = st.text_area("1. 선생님이 내주신 과제")
your_writing = st.text_area("2. 내가 쓴 글")

# 입력 값 검증 및 인공지능 호출
if st.button("개선 사항 생성하기"):
    if not all([assignment, your_writing]):
        st.warning("모든 입력을 작성해주세요!")
    else:
        # 프롬프트 구성
        prompt_parts = [
            "다음은 선생님이 내주신 과제와 내가 쓴 글입니다. 이를 바탕으로 더 조사해야 할 점과 더 적어야 할 점을 제안해주세요.\n\n",
            f"1. 선생님이 내주신 과제: {assignment}",
            f"2. 내가 쓴 글: {your_writing}",
            "\n더 조사해야 할 점과 더 적어야 할 점을 제안해주세요."
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
            st.success("개선 사항 생성 완료!")
            st.text_area("생성된 개선 사항:", value=response_text, height=300)
            st.download_button(label="개선 사항 다운로드", data=response_text, file_name="improvement_suggestions.txt", mime="text/plain")
            st.write("인공지능이 생성한 제안은 꼭 본인이 확인해야 합니다. 생성된 제안을 검토하고, 필요한 경우에만 수정하세요.")
        else:
            st.error("API 호출에 실패했습니다. 나중에 다시 시도해주세요.")

# 세션 초기화 버튼
if st.button("다시 시작하기"):
    st.experimental_rerun()
