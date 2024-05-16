import pathlib
import textwrap
import google.generativeai as genai
import streamlit as st
import toml
from PIL import Image
import io
import random

def to_markdown(text):
    text = text.replace('•', '*')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# 사용방법 안내
st.title("인공지능씨, 내 작품 어때요?")
st.write("""
1. "Browse files"를 클릭합니다.
2. 카메라를 선택하고, 사진을 가로로 찍습니다.
3. 사진이 업로드가 자동으로 됩니다.
4. Running이 끝나면 인공지능이 여러분의 그림을 보고 이야기해줍니다.
5. 인공지능의 반응을 살펴봅시다.
6. 결과와 이미지를 다운로드 해 봅시다.
""")

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
try:
    genai.configure(api_key=selected_api_key)
except Exception as e:
    st.error(f"선택된 API 키로 요청 실패: {e}")

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
  response = model.generate_content(["이 사진은 초등학생이 직접 그린 미술 작품입니다. 그림 이름을 추천해주고, 그린 작품을 자세히 설명해주세요. 장점을 여러개 말해주고, 보완할 점 1가지를 학생이 상처받지 않도록 온화한 화법으로 말해주세요.", img])

  # Resolve the response
  response.resolve()

  # 결과 표시
  st.image(img) # 업로드된 사진 출력
  result_text = response.text  # 결과 텍스트
  st.markdown(result_text)

  # 텍스트 결과를 다운로드 가능한 텍스트 파일로 제공
  txt_to_download = result_text.encode('utf-8')
  st.download_button(label="결과를 다운로드하세요.",
                     data=txt_to_download,
                     file_name="artwork_analysis.txt",
                     mime='text/plain')

  # 이미지 다운로드
  img_bytes_io = io.BytesIO()
  img.save(img_bytes_io, format='JPEG')
  img_bytes_io.seek(0)
  st.download_button(label="이미지 다운로드",
                     data=img_bytes_io,
                     file_name="uploaded_image.jpg",
                     mime="image/jpeg")

else:
  st.markdown("핸드폰 사진을 업로드하세요.")
