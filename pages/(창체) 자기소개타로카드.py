import streamlit as st
from openai import OpenAI
import requests
from io import BytesIO

# 페이지 레이아웃 설정
st.set_page_config(layout="wide")

# 비밀번호 입력
password = st.text_input("비밀번호를 입력하세요:", type="password")
correct_password = st.secrets["password1"]

# 입력된 비밀번호가 정확한지 확인
if password == correct_password:
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
        # API 키 리스트
        api_keys = [st.secrets["api_key1"], st.secrets["api_key2"], st.secrets["api_key3"], st.secrets["api_key4"], st.secrets["api_key5"], st.secrets["api_key6"]]

        # 이미지 생성 프롬프트
        prompt = f"{gender} 아이의 중앙 일러스트레이션과 주변에 좋아하는 물건({likes_items}), 좋아하는 사람({likes_people}), 장래 희망({aspiration}), 지금 하고 싶은 것({want_to_do}), 좋아하는 음식({favorite_food}), 좋아하는 나라({favorite_country})을 둘러싼 타로 카드 디자인. 카드 하단에 '{name}'이라는 이름이 크게 표시됩니다."

        # 이미지 생성 시도
        for api_key in api_keys:
            try:
                # OpenAI 객체 생성 및 API 키 제공
                client = OpenAI(api_key=api_key)

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
                break  # 이미지 생성 성공 시 반복 종료
            except Exception as e:
                st.error(f"{api_key} 사용 중 오류 발생. 다른 키를 시도합니다: " + str(e))
                continue  # 다음 키로 시도
    else:
        st.warning("모든 필드를 채워주세요!")
else:
    st.error("올바른 비밀번호를 입력해주세요.")
