import streamlit as st
import requests
from PIL import Image
import io
import random
import google.generativeai as genai
from openai import OpenAI

# 페이지 레이아웃 설정
st.set_page_config(layout="wide")

# OpenAI API 키 리스트
openai_api_keys = [
    st.secrets["api_key1"],
    st.secrets["api_key2"],
    st.secrets["api_key3"],
    st.secrets["api_key4"],
    st.secrets["api_key5"],
    st.secrets["api_key6"],
    st.secrets["api_key7"],
    st.secrets["api_key8"],
    st.secrets["api_key9"],
    st.secrets["api_key10"],
    st.secrets["api_key11"],
    st.secrets["api_key12"]
]

# Google Generative AI API 키 리스트
genai_api_keys = [
    st.secrets["gemini_api_key1"],
    st.secrets["gemini_api_key2"],
    st.secrets["gemini_api_key3"],
    st.secrets["gemini_api_key4"],
    st.secrets["gemini_api_key5"],
    st.secrets["gemini_api_key6"],
    st.secrets["gemini_api_key7"],
    st.secrets["gemini_api_key8"],
    st.secrets["gemini_api_key9"],
    st.secrets["gemini_api_key10"],
    st.secrets["gemini_api_key11"],
    st.secrets["gemini_api_key12"]
]

# 랜덤하게 OpenAI 및 Google Generative AI API 키 선택
selected_openai_api_key = random.choice(openai_api_keys)
selected_genai_api_key = random.choice(genai_api_keys)

# 함수 정의: 프롬프트를 받아 이미지를 생성하고 표시
def generate_image_from_prompt(prompt, api_key):
    """
    주어진 프롬프트를 사용하여 이미지를 생성하고 Streamlit에 표시하는 함수.
    
    :param prompt: 이미지 생성을 위한 텍스트 프롬프트
    :param api_key: OpenAI API 키
    """
    # OpenAI 객체 생성 및 API 키 제공
    client = OpenAI(api_key=api_key)

    # OpenAI API를 호출하여 이미지 생성
    try:
        image_response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )

        # 생성된 이미지 표시
        generated_image_url = image_response.data[0].url
        st.image(generated_image_url, caption="생성된 이미지")
        
        # 이미지 URL 반환 (필요시 사용하기 위해)
        return generated_image_url
    except Exception as e:
        st.error(f"이미지 생성 중 오류가 발생했습니다: {e}")
        return None

# 함수 정의: 텍스트 프롬프트를 받아 콘텐츠 생성
def try_generate_content(api_key, prompt_parts):
    """
    주어진 프롬프트를 사용하여 콘텐츠를 생성하는 함수.
    
    :param api_key: Google Generative AI API 키
    :param prompt_parts: 콘텐츠 생성을 위한 프롬프트
    :return: 생성된 텍스트 콘텐츠
    """
    # API 키를 설정
    genai.configure(api_key=api_key)
    
    # 설정된 모델 변경
    model = genai.GenerativeModel(
        model_name="gemini-1.0-pro",
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
        ]
    )
    try:
        # 콘텐츠 생성 시도
        response = model.generate_content(prompt_parts)
        return response.text
    except Exception as e:
        # 예외 발생시 None 반환
        st.error(f"API 호출 실패: {e}")
        return None

# 함수 정의: 이미지를 텍스트로 변환
def image_to_text(api_key, img, prompt):
    """
    업로드된 이미지를 텍스트로 변환하는 함수.
    
    :param api_key: Google Generative AI API 키
    :param img: PIL 이미지 객체
    :param prompt: 이미지를 설명하기 위한 텍스트 프롬프트
    :return: 이미지 설명 텍스트
    """
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-pro-vision')

    # Generate content
    try:
        response = model.generate_content([prompt, img])
        # Resolve the response
        response.resolve()
        return response.text
    except Exception as e:
        st.error(f"이미지 설명 생성 중 오류가 발생했습니다: {e}")
        return None

# 사용방법 안내
st.title("📖 만화 다음 컷 생성기")
st.write("""
1. 📂 "Browse files"를 클릭하여 첫 번째 만화 컷 이미지를 업로드하세요.
2. ✍️ 전체 이야기, 주인공, 전체 만화 컷수를 입력하세요.
3. ⏳ '다음 컷 이야기 생성' 버튼을 클릭하고 다음 컷 이야기를 확인하세요.
4. 🖼 '다음 컷 그림 생성' 버튼을 클릭하여 다음 컷 그림을 생성하세요.
""")

st.write("📢 이 앱은 원중초등학교 4학년 1반 한수민 학생의 아이디어로 만들어졌습니다. 🎉👏")

# 세션 초기화 함수
def reset_session_state():
    st.session_state['generated_image_description'] = ""
    st.session_state['generated_next_cut_story'] = ""
    st.session_state['generated_image_url'] = ""

# 세션 초기화 버튼
if st.button("새로 시작하기 - 세션 초기화"):
    reset_session_state()

# 세션 상태 초기화
if 'generated_image_description' not in st.session_state:
    st.session_state['generated_image_description'] = ""
if 'generated_next_cut_story' not in st.session_state:
    st.session_state['generated_next_cut_story'] = ""
if 'generated_image_url' not in st.session_state:
    st.session_state['generated_image_url'] = ""

# 만화 컷 이미지 업로드
uploaded_file = st.file_uploader("만화 업로드")

# 추가 정보 입력받기
story = st.text_area("전체 이야기:")
main_character = st.text_input("주인공 이름:")
image_description_prompt = st.text_area("그린 그림을 설명해주세요.:")

if uploaded_file is not None:
    img_bytes = uploaded_file.read()
    img = Image.open(io.BytesIO(img_bytes))
    st.image(img, caption="업로드된 만화 컷")

    if st.button("인공지능아, 다음 컷은 어떤 이야기가 나올 것 같아?"):
        try:
            # 업로드된 이미지 묘사 생성
            img_description = image_to_text(selected_genai_api_key, img, image_description_prompt)
            st.session_state['generated_image_description'] = img_description
            
            # 이미지 묘사 및 입력받은 이야기 기반으로 다음 컷 이야기 생성
            story_prompt = [
                f"이 만화의 첫 번째 컷입니다. 이미지 묘사는 다음과 같습니다: {img_description}. 전체 이야기는 다음과 같습니다: {story}. 주인공은 {main_character}입니다. 다음 만화 컷의 이야기를 상상해서 설명해 주세요. 구체적인 대화와 행동을 포함해 주세요."
            ]
            next_cut_story = try_generate_content(selected_genai_api_key, story_prompt)
            st.session_state['generated_next_cut_story'] = next_cut_story

        except Exception as e:
            st.error(f"다음 컷 이야기 생성 중 오류가 발생했습니다: {e}")

# 이전 단계에서 생성된 이야기를 출력
if st.session_state['generated_next_cut_story']:
    st.write("다음 이야기:", st.session_state['generated_next_cut_story'])

if st.session_state['generated_next_cut_story']:
    if st.button("다음 그림을 그려주세요."):
        try:
            # 다음 컷 이미지 생성
            generated_image_url = generate_image_from_prompt(st.session_state['generated_next_cut_story'], selected_openai_api_key)
            st.session_state['generated_image_url'] = generated_image_url

        except Exception as e:
            st.error(f"다음 컷 그림 생성 중 오류가 발생했습니다: {e}")

# 생성된 이미지를 다운로드 버튼 표시
if st.session_state['generated_image_url']:
    response = requests.get(st.session_state['generated_image_url'])
    image_bytes = io.BytesIO(response.content)
    st.download_button(label="이미지 다운로드",
                       data=image_bytes,
                       file_name="next_comic_cut.jpg",
                       mime="image/jpeg")
