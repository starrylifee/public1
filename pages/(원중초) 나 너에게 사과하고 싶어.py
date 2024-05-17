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
st.title("💌 타인의 마음을 고려한 편지 쓰기 💌")
st.write("""
1. 📝 아래의 질문에 답을 작성하세요.
2. 📤 모든 답변을 완료한 후 "편지 생성하기" 버튼을 클릭하세요.
3. 💬 인공지능이 여러분의 답변을 바탕으로 편지를 작성해줍니다.
4. 📥 결과를 다운로드하거나, 편지를 수정하여 사용할 수 있습니다.
""")

st.write("📢 이 앱은 원중초등학교 4학년 1반 장서현 학생의 아이디어로 만들어졌습니다. 🎉👏")

# 입력 필드
incident = st.text_area("1. 무슨일이 있었나요?")
reason = st.text_area("2. 왜 이런 일이 일어났다고 생각하나요?")
thoughts = st.text_area("3. 그때 어떤 생각으로 그런 행동을 했나요?")
harm = st.text_area("4. 다른 사람에게 어떤 피해가 있었나요?")
recovery = st.text_area("5. 어떻게 하면 발생한 피해가 회복될 수 있을까요?")
improvements = st.text_area("6. 무엇을 하는 것이 이 상황을 좀 더 좋게 만들 수 있을까요?")
actions = st.text_area("7. 내가 할 수 있는 일은 무엇인가요?")
future_relation = st.text_area("8. 앞으로 그 사람과 어떤 관계가 되고 싶나요?")
feelings = st.text_area("9. 이 일을 겪으면서 느낀 점은 무엇인가요?")

# 입력 값 검증 및 인공지능 호출
if st.button("편지 생성하기"):
    if not all([incident, reason, thoughts, harm, recovery, improvements, actions, future_relation, feelings]):
        st.warning("모든 질문에 답을 작성해주세요!")
    else:
        # 프롬프트 구성
        prompt_parts = [
            "다음 질문들에 대한 답변을 바탕으로 타인의 마음을 고려한 편지를 작성해주세요.\n\n",
            f"1. 무슨일이 있었나요? {incident}",
            f"2. 왜 이런 일이 일어났다고 생각하나요? {reason}",
            f"3. 그때 어떤 생각으로 그런 행동을 했나요? {thoughts}",
            f"4. 다른 사람에게 어떤 피해가 있었나요? {harm}",
            f"5. 어떻게 하면 발생한 피해가 회복될 수 있을까요? {recovery}",
            f"6. 무엇을 하는 것이 이 상황을 좀 더 좋게 만들 수 있을까요? {improvements}",
            f"7. 내가 할 수 있는 일은 무엇인가요? {actions}",
            f"8. 앞으로 그 사람과 어떤 관계가 되고 싶나요? {future_relation}",
            f"9. 이 일을 겪으면서 느낀 점은 무엇인가요? {feelings}",
            "\n이 답변들을 바탕으로 진심을 담아 편지를 작성해주세요."
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
            st.success("편지 생성 완료!")
            st.text_area("생성된 편지:", value=response_text, height=300)
            st.download_button(label="편지 다운로드", data=response_text, file_name="generated_letter.txt", mime="text/plain")
        else:
            st.error("API 호출에 실패했습니다. 나중에 다시 시도해주세요.")

# 세션 초기화 버튼
if st.button("다시 시작하기"):
    st.experimental_rerun()
