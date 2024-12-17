import streamlit as st
import requests
from PIL import Image, UnidentifiedImageError
import io
import random
import google.generativeai as genai
from openai import OpenAI

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

# 사용방법 안내
st.title("🏺 역사 시대 사진 변환 앱")
st.write("""
1. 📂 "Browse files"를 클릭하여 사진을 업로드하세요.
2. ⏳ 원하는 시대를 선택하세요 (구석기, 신석기, 청동기, 철기).
3. ✨ 사진에 대한 추가 묘사를 입력하세요.
4. ⏳ '묘사 생성 및 변환' 버튼을 클릭하세요.
5. 💬 AI가 사진을 선택한 시대의 스타일로 사실적으로 변환합니다.
6. 📥 결과를 확인하고 다운로드해 보세요.
""")

# 시대 선택 라디오 버튼
selected_era = st.radio("시대 선택:", ["구석기", "신석기", "청동기", "철기"], index=0)

# 업로드된 이미지 처리
uploaded_file = st.file_uploader("📸 사진 업로드")

# 추가 묘사 입력
student_description = st.text_input("추가로 넣고 싶은 묘사를 입력하세요:", "")

if uploaded_file is not None:
    img_bytes = uploaded_file.read()
    try:
        img = Image.open(io.BytesIO(img_bytes))
        st.image(img, caption="업로드된 이미지")

        if st.button("묘사 생성 및 변환"):
            with st.spinner("이미지를 선택한 시대에 맞게 변환 중입니다. 잠시만 기다려주세요..."):
                try:
                    # Google Generative AI를 사용해 이미지 묘사 생성
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content([
                        f"이 사진에 나타난 모습이 {selected_era} 시대로 바뀐다고 상상했을 때 의상, 배경, 도구, 문화 등에 맞게 {selected_era} 시기에 해당하는 내용으로 사실적으로 묘사해주세요. "
                        "인물의 의상, 배경에 해당 시대의 주요 특징이 반영되어야 합니다.",
                        img
                    ])
                    response.resolve()
                    ai_description = response.text
                    st.write(f"AI가 생성한 {selected_era} 시대 묘사: ", ai_description)
                    
                    # 최종 묘사 생성
                    final_description = (
                        f"Transform this photo into the {selected_era} era. "
                        f"Include {selected_era} era accurate tools, clothing made of fur or textiles, "
                        f"appropriate natural backgrounds like forests or plains, and no modern elements such as buildings, electronics, or machines. "
                        f"Student request: {student_description.strip()}. Ensure the depiction aligns strictly with historical accuracy."
                    )


                    # OpenAI API 호출
                    image_response = client.images.generate(
                        model="dall-e-3",
                        prompt=f"Photo transformed into {selected_era} era with: {final_description}",
                        size="1024x1024",
                        quality="standard",
                        n=1
                    )

                    # 생성된 이미지 표시
                    generated_image_url = image_response.data[0].url
                    st.image(generated_image_url, caption=f"{selected_era} 시대 스타일 변환 결과")

                    # 이미지 다운로드 준비
                    response = requests.get(generated_image_url)
                    image_bytes = io.BytesIO(response.content)

                    # 이미지 다운로드 버튼
                    st.download_button(label="이미지 다운로드",
                                       data=image_bytes,
                                       file_name=f"{selected_era}_transformed.jpg",
                                       mime="image/jpeg")
                except Exception as e:
                    st.error(f"이미지 생성 중 오류가 발생했습니다: {e}")
    except UnidentifiedImageError:
        st.error("업로드된 파일이 유효한 이미지 파일이 아닙니다. 다른 파일을 업로드해주세요.")
else:
    st.markdown("📸 사진을 업로드하고 시대를 선택하세요.")
