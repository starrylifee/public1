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
st.title("🏃‍♂️ 이 운동을 해보세요! 🏃‍♀️")
st.write("""
1. 📝 아래의 입력 필드에 키, 몸무게, 나이, 성별, 활동 수준, 건강 상태, 운동 선호도를 입력하세요.
2. 🏋️‍♂️ 모든 입력을 완료한 후 "운동 추천 받기" 버튼을 클릭하세요.
3. 💬 인공지능이 여러분에게 적합한 운동을 추천해줍니다.
4. 🔄 '다시 시작하기' 버튼을 눌러 새로운 추천을 받을 수 있습니다.
""")
st.write("📢 이 앱은 서울휘경초등학교 3학년 1반 김성준 학생의 아이디어로 만들어졌습니다. 🎉👏")

# 입력 필드
height = st.number_input("키 (cm)", min_value=100, max_value=200, step=1)
weight = st.number_input("몸무게 (kg)", min_value=20, max_value=100, step=1)
age = st.number_input("나이 (세)", min_value=6, max_value=20, step=1)
gender = st.selectbox("성별", ["남자", "여자"])
activity_level = st.selectbox("활동 수준", ["낮음", "보통", "높음"])
health_condition = st.selectbox("건강 상태", ["건강함", "천식", "알레르기", "과체중", "저체중", "당뇨병"])

# 입력 값 검증 및 인공지능 호출
if st.button("운동 추천 받기"):
    if not all([height, weight, age, gender, activity_level, health_condition]):
        st.warning("모든 입력 필드를 채워주세요!")
    else:
        # 프롬프트 구성
        prompt_parts = [
            "아래는 초등학생에게 적합한 운동을 추천하는 예시입니다.\n입력은 키, 몸무게, 나이, 성별, 활동 수준, 건강 상태, 운동 선호도입니다.\n출력은 추천 운동입니다.\n\n입력을 확인하고 적합한 운동을 추천해주세요. 추천하는 이유도 적어주세요.",
            f"키: {height} cm, 몸무게: {weight} kg, 나이: {age} 세, 성별: {gender}, 활동 수준: {activity_level}, 건강 상태: {health_condition}",
            "추천 운동: "
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
            st.success(f"추천 운동: {response_text}")
        else:
            st.error("API 호출에 실패했습니다. 나중에 다시 시도해주세요.")

# 세션 초기화 버튼
if st.button("다시 시작하기"):
    st.experimental_rerun()
