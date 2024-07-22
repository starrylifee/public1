import pathlib
import textwrap
import google.generativeai as genai
import streamlit as st
import toml
from PIL import Image, UnidentifiedImageError
import io
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

# 사용방법 안내
st.title("🎨 나 이제 색칠해도 될까?")
st.write("""
1. 📜 주제를 입력하세요.
2. 📂 "Browse files"를 클릭합니다.
3. 📷 카메라를 선택하고, 스케치 사진을 찍습니다.
4. 📤 사진이 업로드가 자동으로 됩니다.
5. ⏳ Running이 끝나면 인공지능이 여러분의 스케치를 보고 이야기해줍니다.
6. 💬 인공지능의 반응을 살펴봅시다.
7. 📥 결과와 이미지를 다운로드 해 봅시다.
""")

st.write("📢 이 앱은 서울휘경초등학교 3학년 1반 김채율, 배서윤 학생의 아이디어로 만들어졌습니다. 🎉👏")

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

# 세션 상태를 초기화하는 버튼
if st.button("🔄 새로 시작하기 (눌러주세요!)"):
    st.session_state.clear()
    st.experimental_rerun()

# 그림 주제 입력
subject = st.text_input("그림 주제를 입력하세요:", "")

# 핸드폰 사진 업로드 기능 추가
uploaded_file = st.file_uploader("📱 핸드폰 사진 업로드")

# 이미지가 업로드되었는지 확인
if uploaded_file is not None:
    if subject:
        with st.spinner('AI가 스케치를 분석 중입니다...'):
            try:
                # 이미지 바이트 문자열로 변환
                img_bytes = uploaded_file.read()

                # bytes 타입의 이미지 데이터를 PIL.Image.Image 객체로 변환
                img = Image.open(io.BytesIO(img_bytes))

                model = genai.GenerativeModel('gemini-1.5-flash')

                # Generate content
                response = model.generate_content([
                    f"이 사진은 '{subject}' 주제의 스케치입니다. 초등학생에게 말하는 수준으로 이야기해주세요. '{subject}' 주제와 스케치를 살펴보고 더 좋은 그림을 위해 학생이 보강하면 좋은 부분을 안내해주세요. 또 그려진 스케치에 대한 칭찬도 해주세요.", 
                    img
                ])

                # Resolve the response
                response.resolve()

                # 결과 표시
                st.image(img) # 업로드된 사진 출력
                result_text = response.text  # 결과 텍스트
                st.markdown(result_text)

                # 텍스트 결과를 다운로드 가능한 텍스트 파일로 제공
                txt_to_download = result_text.encode('utf-8')
                st.download_button(label="📄 결과를 다운로드하세요.",
                                   data=txt_to_download,
                                   file_name="sketch_analysis.txt",
                                   mime='text/plain')

                # 이미지 다운로드
                if img.mode != "RGB":
                    img = img.convert("RGB")
                img_bytes_io = io.BytesIO()
                img.save(img_bytes_io, format='JPEG')
                img_bytes_io.seek(0)
                st.download_button(label="🖼️ 이미지 다운로드",
                                   data=img_bytes_io,
                                   file_name="uploaded_sketch.jpg",
                                   mime="image/jpeg")
            except UnidentifiedImageError:
                st.error("업로드된 파일이 유효한 이미지 파일이 아닙니다. 다른 파일을 업로드해 주세요.")
            except Exception as e:
                st.error(f"색상 추천 생성 중 오류가 발생했습니다: {e}")
    else:
        st.warning("먼저 그림 주제를 입력하세요.")
else:
    st.markdown("📱 핸드폰 사진을 업로드하세요.")
    if not subject:
        st.warning("먼저 그림 주제를 입력하세요.")
