import streamlit as st
import toml
import pathlib
from openai import OpenAI

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

# secrets.toml 파일 경로 설정
secrets_path = pathlib.Path(__file__).parent.parent / ".streamlit/secrets.toml"

# secrets.toml 파일 읽기
with open(secrets_path, "r", encoding="utf-8") as f:
    secrets = toml.load(f)

# OpenAI 클라이언트 초기화 (secrets.toml에서 API 키 가져오기)
client = OpenAI(api_key=secrets["api_key7"])

st.title("AI 프롬프트 생성기")

# 사용자 입력 받기 (placeholder 설정)
user_role = st.text_input(
    "사용자의 역할을 입력하세요",
    placeholder="6학년 영어를 가르치는 교사"
)
task = st.text_area(
    "수행할 작업을 입력하세요",
    placeholder="핵심표현을 직접 말하고 쓸 수 있는 과업 생성"
)
context = st.text_area(
    "맥락을 제공하세요",
    placeholder="개인, 짝이 상호작용하는 것을 중요하게 생각함"
)

# 선택 옵션을 위한 접이식 섹션
with st.expander("선택 옵션 추가하기"):
    tone = st.selectbox("형식/어조 선택", ["정중함", "격식 있음", "편안함", "기타"], index=2)
    classroom_context = st.text_area("교실 수업 상황", placeholder="예: 학생들이 조용히 듣고 있는 상황")
    prior_learning = st.text_area("사전 학습 정도", placeholder="예: 학생들이 이미 기본 표현을 학습한 상태")
    learner_state = st.text_area("학습자 상태", placeholder="예: 일부 학생들이 집중력이 부족함")
    expected_result = st.text_area("결과 예시", placeholder="예: 학생들이 간단한 문장을 완성할 수 있어야 함")

# 생성된 프롬프트 표시
if st.button("프롬프트 생성"):
    if user_role and task and context:
        # 추가된 선택 옵션을 포함한 프롬프트 메시지 구성
        additional_context = f"형식/어조: {tone}\n"
        if classroom_context:
            additional_context += f"교실 수업 상황: {classroom_context}\n"
        if prior_learning:
            additional_context += f"사전 학습 정도: {prior_learning}\n"
        if learner_state:
            additional_context += f"학습자 상태: {learner_state}\n"
        if expected_result:
            additional_context += f"결과 예시: {expected_result}\n"

        messages = [
            {"role": "system", "content": "당신은 AI 어시스턴트입니다. 초등학교 교사가 AI가 이해할 수 있는 프롬프트를 생성하는 것을 돕습니다."},
            {"role": "user", "content": f"다음 입력을 명확하고 간결한 프롬프트로 변환해 주세요. 교사의 역할: {user_role}. 수행할 작업: {task}. 이 작업의 맥락: {context}. 추가 정보: {additional_context}"}
        ]

        # OpenAI API 호출
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        # 응답에서 프롬프트 추출
        generated_prompt = response.choices[0].message.content

        # 응답 출력
        st.subheader("생성된 프롬프트:")
        st.write(generated_prompt)
    else:
        st.warning("모든 필수 입력을 완료해주세요.")
