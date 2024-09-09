import streamlit as st
import toml
import pathlib
from openai import OpenAI

# secrets.toml 파일 경로 설정
secrets_path = pathlib.Path(__file__).parent.parent / ".streamlit/secrets.toml"

# secrets.toml 파일 읽기
with open(secrets_path, "r", encoding="utf-8") as f:
    secrets = toml.load(f)

# OpenAI 클라이언트 초기화 (secrets.toml에서 API 키 가져오기)
client = OpenAI(api_key=secrets["api_key7"])

st.title("AI 프롬프트 평가기")

# 사용자가 평가할 프롬프트를 입력받는 필드
prompt = st.text_area(
    "평가할 프롬프트를 입력하세요",
    placeholder="여기에 평가할 프롬프트를 입력하세요"
)

# 평가 버튼
if st.button("평가하기"):
    if prompt:
        # 평가 기준을 설명하는 메시지 작성
        evaluation_prompt = f"""
        다음 프롬프트를 평가해 주세요:
        '{prompt}'
        평가 기준:
        1. 명확성: 이 프롬프트가 인공지능이 이해하기에 얼마나 명확한가요?
        2. 관련성: 이 프롬프트가 학교교사에게 주어진 역할과 작업에 얼마나 관련이 있나요?
        3. 완전성: 이 프롬프트가 학교교사의 업무나 수업을 보조하기에 충분히 완전한가요, 혹은 중요한 요소가 누락되어 있나요?
        4. 실행 가능성: 이 프롬프트가 인공지능이 듣고 실질적으로 실행 가능한가요?
        5. 종합적 품질: 이 프롬프트의 전반적인 품질이 얼마나 높은가요?
        각 기준에 대해 1-10점 사이의 점수를 부여하고, 각 기준에 대한 간단한 피드백을 제공해 주세요. 마지막에는 모든 점수를 더해서 총점을 출력해주세요.
        """

        # OpenAI API 호출
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 교사가 만들어 인공지능에게 보여줄 프롬프트를 평가하는 전문가 입니다."},
                {"role": "user", "content": evaluation_prompt}
            ]
        )

        # 응답에서 평가 결과 추출
        evaluation_result = response.choices[0].message.content

        # 평가 결과 출력
        st.subheader("AI 평가 결과")
        st.write(evaluation_result)
    else:
        st.warning("평가할 프롬프트를 입력하세요.")
