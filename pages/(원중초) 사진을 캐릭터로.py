import streamlit as st
import requests
from PIL import Image
import io
import random
import google.generativeai as genai
from openai import OpenAI

# 페이지 레이아웃 설정
st.set_page_config(layout="wide")

# API 키 리스트
api_keys = [
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

# 랜덤하게 API 키 선택
selected_api_key = random.choice(api_keys)
client = OpenAI(api_key=selected_api_key)

# Google Generative AI 설정
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

selected_genai_api_key = random.choice(genai_api_keys)
genai.configure(api_key=selected_genai_api_key)

# 업로드된 이미지 처리
uploaded_file = st.file_uploader("📱 핸드폰 사진 업로드")

# 학생이 넣고 싶은 묘사 입력받기
student_description = st.text_input("학생이 추가하고 싶은 묘사를 입력하세요:", "")

# 이미지가 업로드되었는지 확인
if uploaded_file is not None:
    img_bytes = uploaded_file.read()
    img = Image.open(io.BytesIO(img_bytes))
    st.image(img, caption="업로드된 이미지")

    if st.button("묘사 생성 및 캐리커쳐 생성"):
        try:
            # Google Generative AI를 사용하여 이미지 묘사 생성
            model = genai.GenerativeModel('gemini-pro-vision')
            response = model.generate_content([
                "이 사진을 자세히 묘사해주세요. 성별, 헤어스타일, 눈코입, 옷, 악세서리, 표정, 피부색, 얼굴형, 나이, 머리카락 길이, 눈색깔, 머리색깔 등을 자세한 표현으로 이야기해주세요.", 
                img
            ])
            response.resolve()
            ai_description = response.text
            st.write("AI가 생성한 이미지 묘사: ", ai_description)
            st.write("오른쪽 위 'Running'이 없어질 때까지 기다려 주세요")
            # 최종 묘사 생성
            final_description = f"{ai_description}. 학생이 추가한 묘사: {student_description}"
            st.write("최종 묘사: ", final_description)

            # OpenAI API를 호출하여 이미지 생성
            image_response = client.images.generate(
                model="dall-e-3",
                prompt=f"Caricature of the person: {final_description}",
                size="1024x1024",
                quality="standard",
                n=1
            )

            # 생성된 이미지 표시
            generated_image_url = image_response.data[0].url
            st.image(generated_image_url, caption="생성된 캐리커쳐")

            # 이미지 다운로드 준비
            response = requests.get(generated_image_url)
            image_bytes = io.BytesIO(response.content)

            # 이미지 다운로드 버튼
            st.download_button(label="이미지 다운로드",
                               data=image_bytes,
                               file_name="caricature.jpg",
                               mime="image/jpeg")
        except Exception as e:
            st.error(f"이미지 생성 중 오류가 발생했습니다: {e}")
else:
    st.markdown("📱 핸드폰 사진을 업로드하세요.")
