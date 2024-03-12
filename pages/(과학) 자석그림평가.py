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
gemini_api_key2 = secrets["gemini_api_key2"]

# Gemini API 키 설정
genai.configure(api_key=gemini_api_key2)

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
  response = model.generate_content(["이 사진은 책상위에 올려둔 나침반의 바늘이 움직이다 멈추었을 때 어느방향을 가르키는지 쓰고, 그 까닭을 그림으로 나타낸 작품입니다. 평가기준 1: '자석의 N극은 북쪽, S극은 남쪽을 가리킨다'는 그림이 들어가 있으면 10점을 주고, 둘중 하나만 있는 경우에는 5점을 주세요. 평가기준 2: '지구가 하나의 자석과 같은 성질이 있다, 지구의 북극쪽이 S극 지구의 남극쪽이 N극의 성질을 나타낸다'는 그림이 들어가면 추가로 10점을 주세요. 평가기준은 2개이며 각각 10점 만점으로 총점 20점 만점입니다. 평가기준과 기준별 획득점수도 설명과 함께 출력해주세요.", img])

  # Resolve the response
  response.resolve()

  # 결과 표시
  st.image(img) # 업로드된 사진 출력
  st.markdown(response.text)
else:
  st.markdown("핸드폰 사진을 업로드하세요.")