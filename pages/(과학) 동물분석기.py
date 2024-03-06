import pathlib
import textwrap
import google.generativeai as genai
import streamlit as st
import toml
from PIL import Image
import io

def to_markdown(text):
    text = text.replace('•', '*')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# secrets.toml 파일 경로
secrets_path = pathlib.Path(__file__).parent.parent / ".streamlit/secrets.toml"

# secrets.toml 파일 읽기
with open(secrets_path, "r") as f:
    secrets = toml.load(f)

# secrets.toml 파일에서 gemini_api_key1 값 가져오기
gemini_api_key1 = secrets["gemini_api_key1"]

# Gemini API 키 설정
genai.configure(api_key=gemini_api_key1)

# 핸드폰 사진 업로드 기능 추가
uploaded_file = st.file_uploader("핸드폰 사진 업로드")

# 이미지가 업로드되었는지 확인
if uploaded_file is not None:
  # 이미지 바이트 문자열로 변환
  img_bytes = uploaded_file.read()

  # bytes 타입의 이미지 데이터를 PIL.Image.Image 객체로 변환
  img = Image.open(io.BytesIO(img_bytes))

  model = genai.GenerativeModel('gemini-pro-vision')

  # Generate content
  response = model.generate_content(["이 사진은 동물의 사진입니다. 동물의 모습과 습성, 서식지 등을 학생에게 설명하듯이 자세히 설명해준 뒤 마지막에 어떤 동물인지 판별해주세요.", img])

  # Resolve the response
  response.resolve()

  # 결과 표시
  st.image(img) # 업로드된 사진 출력
  st.markdown(response.text)
else:
  st.markdown("핸드폰 사진을 업로드하세요.")