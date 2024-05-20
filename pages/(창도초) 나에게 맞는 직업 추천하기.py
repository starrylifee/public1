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

# Streamlit 앱 인터페이스 구성
st.title("🔍 나에게 맞는 직업 추천하기 🔍")
st.write("""
1. 📋 좋아하는 활동, 성격, 자신 있는 것, 자신 없는 것, MBTI 등을 선택하세요.
2. 📤 모든 입력을 완료한 후 "직업 추천 받기" 버튼을 클릭하세요.
3. 💬 인공지능이 여러분의 입력을 바탕으로 추천 직업 5개와 이유를 제안해줍니다.
4. 📥 결과를 다운로드하거나, 제안을 수정하여 사용할 수 있습니다.
""")

st.write("📢 이 앱은 창도초등학교 5학년 5반 김은성 학생의 아이디어로 만들어졌습니다. 🎉👏")

# 상태 관리 변수 설정
if 'activities' not in st.session_state:
    st.session_state['activities'] = []
if 'personality' not in st.session_state:
    st.session_state['personality'] = ""
if 'strengths' not in st.session_state:
    st.session_state['strengths'] = ""
if 'weaknesses' not in st.session_state:
    st.session_state['weaknesses'] = ""
if 'mbti' not in st.session_state:
    st.session_state['mbti'] = ""

# 입력 필드
activities = st.multiselect("좋아하는 활동", ["운동", "음악 감상", "독서", "여행", "요리", "게임", "미술", "공예"], default=st.session_state['activities'])
personality = st.selectbox("나의 성격", ["외향적", "내향적", "논리적", "감정적", "현실적", "이상적"], index=0 if st.session_state['personality'] == "" else ["외향적", "내향적", "논리적", "감정적", "현실적", "이상적"].index(st.session_state['personality']))
strengths = st.text_area("내가 자신 있는 것", value=st.session_state['strengths'])
weaknesses = st.text_area("내가 자신 없는 것", value=st.session_state['weaknesses'])
mbti = st.selectbox("MBTI", ["ESTJ", "ESFJ", "ENTJ", "ENFJ", "ISTJ", "ISFJ", "INTJ", "INFJ", "ESTP", "ESFP", "ENTP", "ENFP", "ISTP", "ISFP", "INTP", "INFP"], index=0 if st.session_state['mbti'] == "" else ["ESTJ", "ESFJ", "ENTJ", "ENFJ", "ISTJ", "ISFJ", "INTJ", "INFJ", "ESTP", "ESFP", "ENTP", "ENFP", "ISTP", "ISFP", "INTP", "INFP"].index(st.session_state['mbti']))

# 입력 값 검증 및 인공지능 호출
if st.button("직업 추천 받기"):
    if not all([activities, personality, strengths, weaknesses, mbti]):
        st.warning("모든 입력을 작성해주세요!")
    else:
        # 입력값을 상태 변수에 저장
        st.session_state['activities'] = activities
        st.session_state['personality'] = personality
        st.session_state['strengths'] = strengths
        st.session_state['weaknesses'] = weaknesses
        st.session_state['mbti'] = mbti

        # 프롬프트 구성
        prompt_parts = [
            "다음은 사용자에 대한 정보입니다. 이 정보를 바탕으로 추천 직업 5개와 이유를 제안해주세요.\n\n",
            f"1. 좋아하는 활동: {', '.join(activities)}",
            f"2. 나의 성격: {personality}",
            f"3. 내가 자신 있는 것: {strengths}",
            f"4. 내가 자신 없는 것: {weaknesses}",
            f"5. MBTI: {mbti}",
            "\n추천 직업 5개와 이유를 제안해주세요."
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
            st.success("직업 추천 완료!")
            st.text_area("추천된 직업:", value=response_text, height=300)
            st.download_button(label="직업 추천 다운로드", data=response_text, file_name="recommended_jobs.txt", mime="text/plain")
            st.write("인공지능이 생성한 추천 직업을 꼭 본인이 확인하세요. 생성된 추천 직업을 검토하고, 필요한 경우 수정하세요.")
        else:
            st.error("API 호출에 실패했습니다. 나중에 다시 시도해주세요.")

# 세션 초기화 버튼
if st.button("다시 시작하기"):
    st.session_state['activities'] = []
    st.session_state['personality'] = ""
    st.session_state['strengths'] = ""
    st.session_state['weaknesses'] = ""
    st.session_state['mbti'] = ""
    st.experimental_rerun()
