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
st.title("이 음식은 어떤 음식인가요?")
st.write("""
1. "Browse files"를 클릭합니다.
2. 카메라를 선택하고, 음식 사진을 찍습니다.
3. 사진이 업로드가 자동으로 됩니다.
4. Running이 끝나면 인공지능이 여러분의 음식을 보고 이야기해줍니다.
5. 인공지능의 반응을 살펴봅시다.
6. 결과와 이미지를 다운로드 해 봅시다.
""")
st.write("📢 이 앱은 서울휘경초등학교 3학년 1반 박태이 학생의 아이디어로 만들어졌습니다. 🎉👏")


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
    response = model.generate_content(["이 사진은 음식입니다. 초등학생에게 말하는 수준으로 이 음식의 영양소를 안내해주고, 알레르기 정보를 알려주세요. 과잉 섭취에 대한 경고와 특정 질병과의 연관성도 안내해주세요. 또한, 이 음식의 역사나 기원에 대해서도 설명해주세요.", img])

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
                       file_name="food_analysis.txt",
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
