import streamlit as st
import requests
import google.generativeai as genai
import toml
import random
import pathlib
import urllib.parse
import urllib.request
import json
from bs4 import BeautifulSoup

# 프로젝트 루트 디렉토리 설정
base_path = pathlib.Path(__file__).parent.parent

# secrets.toml 파일 경로
secrets_path = base_path / ".streamlit" / "secrets.toml"

# secrets.toml 파일 읽기
try:
    with open(secrets_path, "r") as f:
        secrets = toml.load(f)
except FileNotFoundError:
    st.error(f"secrets.toml 파일을 찾을 수 없습니다: {secrets_path}")
    st.stop()
except Exception as e:
    st.error(f"secrets.toml 파일을 읽는 중 오류가 발생했습니다: {e}")
    st.stop()

# 네이버 API 키 설정
naver_client_id = secrets.get("naver_client_id")
naver_client_secret = secrets.get("naver_client_secret")

# OpenAI API 키 설정
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

selected_api_key = random.choice(api_keys)

# OpenAI 설정
genai.configure(api_key=selected_api_key)

# 네이버 백과사전 검색 함수
def search_naver_encyclopedia(query):
    encText = urllib.parse.quote(query)
    url = f"https://openapi.naver.com/v1/search/encyc.json?query={encText}"
    headers = {
        "X-Naver-Client-Id": naver_client_id,
        "X-Naver-Client-Secret": naver_client_secret
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        items = response.json().get('items', [])
        return items[0] if items else None
    else:
        return None

# HTML 태그 제거 함수
def remove_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

# OpenAI GPT 호출 함수
def simplify_text(text):
    prompt = f"다음 글을 초등학생이 이해하기 쉽게 요약해 주세요. 글은 2000자 쯤으로 작성해주세요.:\n\n{text}"
    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                  generation_config={
                                      "temperature": 0.7,
                                      "top_p": 0.9,
                                      "max_output_tokens": 2000  # 글자 수를 제한하기 위해
                                  })
    try:
        response = model.generate_content([prompt])
        return response.text.strip()
    except Exception as e:
        print(f"API 호출 실패: {e}")
        return "요약 생성에 실패했습니다."

# 스트림릿 앱 구성
st.title("📖 초등학생을 위한 쉬운 사회 조사 학습 📖")
st.write("""
1. 🔍 조사하고 싶은 주제를 입력하세요.
2. 📚 '검색하기' 버튼을 클릭하세요.
3. 💡 네이버 백과사전의 내용을 가져와 초등학생이 이해하기 쉽게 번역하여 보여드립니다.
""")

st.write("📢 이 앱은 창도초등학교 5학년 5반 이소망 학생의 아이디어로 만들어졌습니다. 🎉👏")

query = st.text_input("조사할 주제")

if st.button("검색하기"):
    if query:
        # 네이버 백과사전 검색
        item = search_naver_encyclopedia(query)
        if item:
            st.write(f"### 제목: {remove_html_tags(item['title'])}")
            st.write(f"#### 링크: [Link]({item['link']})")
            original_text = remove_html_tags(item['description'])
            st.write(f"#### 원본 내용: {original_text}")
            # OpenAI GPT로 요약
            simplified_text = simplify_text(original_text)
            st.write("#### 쉽게 번역된 내용")
            st.write(simplified_text)
        else:
            st.warning("검색 결과가 없습니다.")
    else:
        st.warning("조사할 주제를 입력해주세요!")

# 세션 초기화 버튼
if st.button("다시 시작하기"):
    st.experimental_rerun()
