import os
import streamlit as st
from langchain_teddynote import logging
from langchain_openai import ChatOpenAI

# Streamlit secrets 로드
try:
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    langchain_api_key = st.secrets["LANGCHAIN_API_KEY"]
    langchain_tracing_v2 = st.secrets["LANGCHAIN_TRACING_V2"]
    langchain_endpoint = st.secrets["LANGCHAIN_ENDPOINT"]
    langchain_project = st.secrets["LANGCHAIN_PROJECT"]

    print(f"[OPENAI API KEY]\n{openai_api_key}")
    print(f"[LANGCHAIN API KEY]\n{langchain_api_key}")
    print(f"[LANGCHAIN TRACING V2]\n{langchain_tracing_v2}")
    print(f"[LANGCHAIN ENDPOINT]\n{langchain_endpoint}")
    print(f"[LANGCHAIN PROJECT]\n{langchain_project}")
except KeyError as e:
    st.error(f"환경 변수가 설정되지 않았습니다: {e}")

# LangChain 프로젝트 이름을 설정합니다.
try:
    logging.langsmith(langchain_project)
    print("LangChain 프로젝트 이름이 성공적으로 설정되었습니다.")
except Exception as e:
    st.error(f"LangChain 프로젝트 이름 설정 중 오류가 발생했습니다: {e}")

# ChatOpenAI 객체 생성
try:
    llm = ChatOpenAI(
        temperature=0.9,  # 창의성 (0.0 ~ 2.0)
        max_tokens=2048,  # 최대 토큰수
        model_name="gpt-4o",  # 모델명
        openai_api_key=openai_api_key  # API 키 설정
    )
    print("ChatOpenAI 객체가 성공적으로 생성되었습니다.")
except Exception as e:
    st.error(f"ChatOpenAI 객체 생성 중 오류가 발생했습니다: {e}")

# few-shot 프롬프트 구성 함수
def try_generate_content(prompt_parts):
    prompt = "\n".join(prompt_parts)
    try:
        response = llm.invoke(prompt)
        return response
    except Exception as e:
        st.error(f"API 호출 실패: {e}")
        return None

# 스트림릿 앱 인터페이스 구성
st.title("💌 너에게 사과하고 싶어 💌")
st.write("""
1. 📝 아래의 질문에 답을 작성하세요.
2. 📤 모든 답변을 완료한 후 "편지 생성하기" 버튼을 클릭하세요.
3. 💬 인공지능이 여러분의 답변을 바탕으로 편지를 작성해줍니다.
4. 📥 결과를 다운로드하거나, 편지를 수정하여 사용할 수 있습니다.
""")

st.write("📢 이 앱은 원중초등학교 4학년 1반 장서현 학생의 아이디어로 만들어졌습니다. 🎉👏")

st.markdown("### 아래 질문은 회복적 질문을 바탕으로 한 질문입니다.")

# 입력 필드
incident = st.text_area("1. 무슨 일이 있었나요?")
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
            f"1. 무슨 일이 있었나요? {incident}",
            f"2. 왜 이런 일이 일어났다고 생각하나요? {reason}",
            f"3. 그때 어떤 생각으로 그런 행동을 했나요? {thoughts}",
            f"4. 그 사람에게 어떤 피해가 있었나요? {harm}",
            f"5. 어떻게 하면 발생한 피해가 회복될 수 있을까요? {recovery}",
            f"6. 무엇을 하는 것이 이 상황을 좀 더 좋게 만들 수 있을까요? {improvements}",
            f"7. 내가 할 수 있는 일은 무엇인가요? {actions}",
            f"8. 앞으로 그 사람과 어떤 관계가 되고 싶나요? {future_relation}",
            f"9. 이 일을 겪으면서 느낀 점은 무엇인가요? {feelings}",
            "\n이 답변들을 바탕으로 진심을 담아 편지를 작성해주세요."
        ]

        # API 호출 시도
        response_text = try_generate_content(prompt_parts)

        # 결과 출력
        if response_text is not None:
            st.success("편지 생성 완료!")
            st.text_area("생성된 편지:", value=response_text, height=300)
            st.download_button(label="편지 다운로드", data=response_text, file_name="generated_letter.txt", mime="text/plain")
            st.write("인공지능이 생성한 편지는 꼭 본인이 확인해야 합니다. 생성된 편지를 검토하고, 필요한 경우 수정하세요.")
        else:
            st.error("API 호출에 실패했습니다. 나중에 다시 시도해주세요.")

# 세션 초기화 버튼
if st.button("다시 시작하기"):
    st.experimental_rerun()
