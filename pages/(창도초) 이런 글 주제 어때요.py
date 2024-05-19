import streamlit as st
import random
from datetime import datetime, timedelta
import pathlib
import toml
import google.generativeai as genai

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

# 현재 계절을 반환하는 함수
def get_current_season():
    month = datetime.now().month
    if month in [12, 1, 2]:
        return "겨울"
    elif month in [3, 4, 5]:
        return "봄"
    elif month in [6, 7, 8]:
        return "여름"
    else:
        return "가을"

# 현재 기념일 및 이벤트를 반환하는 함수
def get_current_events():
    today = datetime.now().date()
    event_dates = {
        "새해": datetime(today.year, 1, 1).date(),
        "삼일절": datetime(today.year, 3, 1).date(),
        "어린이날": datetime(today.year, 5, 5).date(),
        "현충일": datetime(today.year, 6, 6).date(),
        "광복절": datetime(today.year, 8, 15).date(),
        "개천절": datetime(today.year, 10, 3).date(),
        "한글날": datetime(today.year, 10, 9).date(),
        "성탄절": datetime(today.year, 12, 25).date()
    }
    for event, event_date in event_dates.items():
        if today >= event_date - timedelta(days=10) and today <= event_date + timedelta(days=10):
            return event
    return None

# 글감 생성 함수
def generate_prompts(season, event):
    base_prompts = [
        f"{season}에 즐길 수 있는 활동들에 대해 써보세요.",
        f"{season}에 나는 무엇을 하는지 이야기해보세요.",
        f"{season} 방학에 무엇을 할 계획인지 이야기해보세요.",
        f"{season}에 가장 기억에 남는 날에 대해 이야기해보세요.",
        f"{season}에 대한 나만의 추억을 이야기해보세요.",
        "자신이 좋아하는 계절과 그 이유에 대해 써보세요.",
        f"{season}에 먹고 싶은 음식에 대해 써보세요.",
        f"{season}에 하고 싶은 활동 리스트를 만들어 보세요."
    ]
    
    if event:
        event_prompts = [
            f"{event}에 대해 알고 있는 것을 써보세요.",
            f"{event}을(를) 맞이하여 특별한 날을 보낸다면 무엇을 하고 싶은지 써보세요.",
            f"{event}의 의미와 중요성에 대해 써보세요.",
            f"가족과 함께 보낸 {event}에 대한 추억을 이야기해보세요.",
            f"{event}과 관련된 전통이나 관습에 대해 써보세요."
        ]
        base_prompts.extend(event_prompts)
    
    return base_prompts

# 스트림릿 앱 인터페이스 구성
st.title("✍️ 계절 주제 글감 생성기 ✍️")
st.write("""
1. 🌟 '글감 생성하기' 버튼을 클릭하세요.
2. 📝 초등학생이 글짓기할 글감을 5개 출력합니다.
3. 📅 계절과 한국 달력 상 기념일 및 이벤트를 고려합니다.
""")

st.write("📢 이 앱은 창도초등학교 5학년 5반 이서현 학생의 아이디어로 만들어졌습니다. 🎉👏")

# 상태 관리 변수 설정
if 'current_season' not in st.session_state:
    st.session_state['current_season'] = ""
if 'current_event' not in st.session_state:
    st.session_state['current_event'] = ""

if st.button("글감 생성하기"):
    current_season = get_current_season()
    current_event = get_current_events()
    
    # 상태 변수에 저장
    st.session_state['current_season'] = current_season
    st.session_state['current_event'] = current_event
    
    if current_event:
        st.write(f"오늘은 {current_event}과(와) 가까운 날입니다! 이를 고려한 글감을 생성합니다. 오른쪽 위 'running'이 끝날 때 까지 기다리세요.")
    else:
        st.write(f"현재 계절은 {current_season}입니다! 이를 고려한 글감을 생성합니다. 오른쪽 위 'running'이 끝날 때 까지 기다리세요.")
    
    example_prompts = generate_prompts(current_season, current_event)
    
    # 인공지능 호출
    prompt_parts = [
        "다음 주제에 대해 초등학생이 글짓기할 수 있는 글감을 5개 생성해주세요.\n\n",
        "예시 프롬프트:\n",
        "\n".join(example_prompts)
    ]
    
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
        st.success("글감 생성 완료!")
        st.text_area("생성된 글감:", value=response_text, height=300)
        st.download_button(label="글감 다운로드", data=response_text, file_name="generated_prompts.txt", mime="text/plain")
        st.write("인공지능이 생성한 글감을 꼭 본인이 확인하세요. 생성된 글감을 검토하고, 필요한 경우 수정하세요.")
    else:
        st.error("API 호출에 실패했습니다. 나중에 다시 시도해주세요.")

# 세션 초기화 버튼
if st.button("다시 시작하기"):
    st.session_state['current_season'] = ""
    st.session_state['current_event'] = ""
    st.experimental_rerun()
