import pathlib
import textwrap
import google.generativeai as genai
import streamlit as st
import toml
from PIL import Image, UnidentifiedImageError
import io
from openai import OpenAI
import random

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

def to_markdown(text):
    text = text.replace('•', '*')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# secrets.toml 파일 경로
secrets_path = pathlib.Path(__file__).parent.parent / ".streamlit/secrets.toml"

# secrets.toml 파일 읽기
with open(secrets_path, "r") as f:
    secrets = toml.load(f)

# secrets.toml 파일에서 API 키 값 가져오기
gemini_api_key1 = secrets.get("gemini_api_key1")
gemini_api_key2 = secrets.get("gemini_api_key2")

# secrets.toml 파일에서 여러 API 키 값 가져오기
api_keys = [
    secrets.get("api_key7"),
    secrets.get("api_key8"),
    secrets.get("api_key9"),
    secrets.get("api_key10"),
    secrets.get("api_key11"),
    secrets.get("api_key12")
]

# 랜덤하게 API 키를 선택하여 OpenAI 클라이언트 초기화
selected_api_key = random.choice(api_keys)
try:
    client = OpenAI(api_key=selected_api_key)
except Exception as e:
    st.error(f"선택된 API 키 {selected_api_key}로 요청 실패: {e}")

# generativeai 함수 설정
def try_generate_text_content(api_key, prompt_parts):
    # API 키를 설정
    genai.configure(api_key=api_key)
    
    # 설정된 모델 변경
    model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                                  generation_config={
                                      "temperature": 0.9,
                                      "top_p": 1,
                                      "top_k": 1,
                                      "max_output_tokens": 1024,
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

def try_generate_content(api_key, image):
    # API 키를 설정
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    try:
        # 콘텐츠 생성 시도
        response = model.generate_content([
            "이 사진은 화석표본입니다. 화석의 이름을 말해주고, 화석 생물이 살았던 모습도 자세히 묘사해주세요.", image
        ])
        response.resolve()
        return response
    except Exception as e:
        # 예외 발생시 None 반환
        print(f"API 호출 실패: {e}")
        return None

# 핸드폰 사진 업로드 기능 추가
uploaded_file = st.file_uploader("핸드폰으로 화석표본을 가로로 찍어주세요.")

# 이미지가 업로드되었는지 확인
if uploaded_file is not None:
    with st.spinner("이미지를 분석중입니다. 잠시만 기다려주세요..."):
        try:
            # 이미지 바이트 문자열로 변환
            img_bytes = uploaded_file.read()

            # bytes 타입의 이미지 데이터를 PIL.Image.Image 객체로 변환
            img = Image.open(io.BytesIO(img_bytes))

            # 첫 번째 API 키로 시도
            response = try_generate_content(gemini_api_key1, img)
            
            # 첫 번째 API 키 실패 시, 두 번째 API 키로 재시도
            if response is None and gemini_api_key2 is not None:
                print("첫 번째 API 호출에 실패하여 두 번째 API 키로 재시도합니다.")
                response = try_generate_content(gemini_api_key2, img)
            
            # 결과가 성공적으로 반환되었는지 확인
            if response is not None:
                # 결과 표시
                st.image(img)  # 업로드된 사진 출력
                st.markdown(response.text)
            else:
                st.markdown("API 호출에 실패했습니다. 나중에 다시 시도해주세요.")
        except UnidentifiedImageError:
            st.error("업로드된 파일이 유효한 이미지 파일이 아닙니다. 다른 파일을 업로드해 주세요.")
else:
    st.markdown("핸드폰 사진을 업로드하세요.")
