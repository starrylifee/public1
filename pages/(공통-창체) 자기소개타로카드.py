import streamlit as st
from openai import OpenAI
import requests
from io import BytesIO
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

st.title("당신의 타로 카드 만들기")
st.header("학생 자기소개")

# 사용자 입력
name = st.text_input("이름을 이니셜로 입력하세요. 예) J.Y.S.:")
gender = st.radio("성별:", ('남자', '여자'))
age = st.slider("나이:", 5, 30)
likes_items = st.text_input("좋아하는 물건을 입력하세요 (쉼표로 구분, 최대 3개):")
likes_people = st.text_input("좋아하는 사람을 입력하세요 (쉼표로 구분, 최대 3개):")
aspiration = st.text_input("장래 희망을 입력하세요:")
want_to_do = st.text_input("지금 하고 싶은 것을 입력하세요:")
favorite_food = st.text_input("가장 좋아하는 음식을 입력하세요:")
favorite_country = st.text_input("가장 좋아하는 나라를 입력하세요:")

generate_button = st.button("타로 카드 생성")

if generate_button and all([name, gender, likes_items, likes_people, aspiration, want_to_do, favorite_food, favorite_country]):
    # 이미지 생성 프롬프트
    prompt = f"{gender} 아이의 중앙 일러스트레이션과 주변에 좋아하는 물건({likes_items}), 좋아하는 사람({likes_people}), 장래 희망({aspiration}), 지금 하고 싶은 것({want_to_do}), 좋아하는 음식({favorite_food}), 좋아하는 나라({favorite_country})을 둘러싼 타로 카드 디자인. 카드 하단에 '{name}'이라는 이름이 크게 표시됩니다."

    try:
        # OpenAI 객체 생성 및 API 키 제공
        client = OpenAI(api_key=selected_api_key)

        # OpenAI API를 호출하여 이미지 생성
        image_response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1792",
            quality="standard",
            n=1
        )

        # 생성된 이미지 표시
        generated_image_url = image_response.data[0].url
        st.image(generated_image_url, caption=f"{name}의 타로 카드")

        # 이미지 다운로드 준비
        response = requests.get(generated_image_url)
        image_bytes = BytesIO(response.content)

        # 이미지 다운로드 버튼
        st.download_button(label="이미지 다운로드",
                            data=image_bytes,
                            file_name=f"{name}_tarot_card.jpg",
                            mime="image/jpeg")
    except Exception as e:
        st.error("현재 사용 중인 키로 오류가 발생했습니다. " + str(e))
else:
    st.warning("모든 필드를 채워주세요!")