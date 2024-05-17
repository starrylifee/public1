import streamlit as st
from openai import OpenAI
import requests
from io import BytesIO
import random

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

# 사용방법 안내
st.title("🎨 종이 인형 옷 생성기")
st.write("""
1. 📜 옷 종류, 색상, 패턴, 악세서리 등을 선택하세요.
2. 📤 모든 옵션을 선택한 후 "종이 인형 옷 생성" 버튼을 클릭하세요.
3. 💬 인공지능이 여러분의 선택을 바탕으로 종이 인형 옷을 생성해줍니다.
4. 📥 결과 이미지를 다운로드할 수 있습니다.
""")

st.write("📢 이 앱은 원중초등학교 4학년 1반 채은서 학생의 아이디어로 만들어졌습니다. 🎉👏")

st.header("종이 인형 옷을 만들어보세요!")

# 옵션 목록
outfit_types = ["원피스", "티셔츠", "바지", "치마", "코트", "자켓", "가디건", "운동복", "잠옷"]
colors = ["빨강", "파랑", "노랑", "초록", "검정", "흰색", "분홍", "보라", "갈색", "회색", "주황"]
patterns = ["스트라이프", "도트", "꽃무늬", "기하학적 패턴", "단색", "체크무늬", "애니메이션 캐릭터"]
accessories_list = ["리본", "레이스", "단추", "주머니", "프릴", "벨트", "스카프", "모자", "귀걸이", "목걸이"]
seasons = ["봄", "여름", "가을", "겨울"]
themes = ["캐주얼", "정장", "파티", "전통", "스포츠", "휴양지", "할로윈", "크리스마스", "여행", "학교"]
fabrics = ["면", "실크", "데님", "니트", "레이스", "폴리에스터", "가죽", "울", "린넨"]
styles = ["모던", "클래식", "빈티지", "펑크", "보헤미안", "고딕", "프레피"]

# 사용자 입력
outfit_type = st.selectbox("옷 종류를 선택하세요:", outfit_types)
color = st.selectbox("원하는 색상을 선택하세요:", colors)
pattern = st.selectbox("원하는 패턴을 선택하세요:", patterns)
accessories = st.multiselect("장식 또는 악세서리를 선택하세요:", accessories_list)
season = st.selectbox("계절을 선택하세요:", seasons)
theme = st.selectbox("테마를 선택하세요:", themes)
fabric = st.selectbox("원단을 선택하세요:", fabrics)
style = st.selectbox("스타일을 선택하세요:", styles)

generate_button = st.button("종이 인형 옷 생성")

if generate_button:
    # 선택된 옵션을 기반으로 프롬프트 생성
    accessories_str = ", ".join(accessories)
    prompt = (
        f"A paper doll outfit designed for {season} season, following a {theme} theme. "
        f"The outfit is a {outfit_type} made from {fabric} fabric, in {color} color with a {pattern} pattern. "
        f"It is decorated with {accessories_str} and follows a {style} style. "
        f"Please include tabs for attachment to a paper doll."
    )

    try:
        # OpenAI 객체 생성 및 API 키 제공
        client = OpenAI(api_key=selected_api_key)

        # OpenAI API를 호출하여 이미지 생성
        image_response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )

        # 생성된 이미지 표시
        generated_image_url = image_response.data[0].url
        st.image(generated_image_url, caption=f"{outfit_type} 옷")

        # 이미지 다운로드 준비
        response = requests.get(generated_image_url)
        image_bytes = BytesIO(response.content)

        # 이미지 다운로드 버튼
        st.download_button(label="이미지 다운로드",
                           data=image_bytes,
                           file_name=f"{outfit_type}_outfit.png",
                           mime="image/png")
    except Exception as e:
        st.error(f"현재 사용 중인 키로 오류가 발생했습니다: {e}")
