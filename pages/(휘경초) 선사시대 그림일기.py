import streamlit as st
import requests
from PIL import Image, UnidentifiedImageError
import io
import random
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

# 사용방법 안내
st.title("🎖️ 선사시대 일기와 그림 생성 ")
st.write("""
1. 🖼️ 구석기, 신석기, 청동기 시대에 대해 학습한 내용을 바탕으로 간단한 글을 작성하세요.
2. ✍️ 인공지능이 글의 내용을 분석하여 옳고 그름을 판단합니다.
3. ⏳ '글 분석 및 일기와 그림 생성' 버튼을 클릭하고 오른쪽 위 'Running'이 없어질 때까지 기다려 주세요.
4. 💬 인공지능이 글을 평가하고, 수정할 부분이 있다면 수정 후 다시 버튼을 눌러주세요.
5. 📥 결과를 다운로드 해 봅시다.
""")

st.write("📢 이 앱은 선사시대에 대해 학습한 내용을 복습하기 위한 학습 도구입니다. 🎓")

# 구석기, 신석기, 청동기 시대 선택 라디오 버튼
selected_era = st.radio(
    "어느 시대에 대해 작성하시겠습니까?",
    ("구석기", "신석기", "청동기")
)

# 학생이 작성한 글 입력받기
student_text = st.text_area(f"{selected_era} 시대에 대해 배운 내용을 적어보세요:", "")

# 버튼 추가
if st.button("글 분석 및 일기와 그림 생성"):
    if not student_text:
        st.warning("⚠️ 내용을 입력해 주세요.")
    else:
        with st.spinner("글 분석 및 일기와 그림 생성 중입니다. 잠시만 기다려주세요..."):
            try:
                # OpenAI API를 사용하여 글의 옳고 그름 판단
                completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": f"학생이 작성한 글: {student_text}. 이 글에서 {selected_era} 시대와 관련된 내용이 옳은지 판단해 주세요. 잘못된 부분이 있다면 수정하거나 설명해 주세요."}
                    ]
                )
                ai_feedback = completion.choices[0].message.content.strip()
                st.write("AI의 글 평가: ", ai_feedback)

                # 수정 요청이 있을 경우 학생이 다시 수정하도록 유도
                if "수정" in ai_feedback or "잘못" in ai_feedback:
                    st.warning("⚠️ AI가 지적한 부분을 수정한 후 다시 시도해 주세요.")
                else:
                    # 최종 일기 생성
                    final_journal_prompt = f"학생이 작성한 글을 바탕으로 {selected_era} 시대에 대한 일기를 작성해 주세요: {student_text}."

                    # OpenAI API를 호출하여 일기와 그림 생성
                    completion = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": final_journal_prompt}
                        ]
                    )
                    journal_text = completion.choices[0].message.content.strip()
                    st.write("AI가 생성한 일기: ", journal_text)

                    # 그림 생성 프롬프트
                    final_description = f"{student_text}. 이 내용을 바탕으로 {selected_era} 시대 사람들의 생활을 묘사한 그림을 그려주세요."

                    # OpenAI API를 호출하여 이미지 생성
                    image_response = client.images.generate(
                        model="dall-e-3",
                        prompt=f"Prehistoric scene: {final_description}",
                        size="1024x1024",
                        quality="standard",
                        n=1
                    )

                    # 생성된 이미지 표시
                    generated_image_url = image_response.data[0].url
                    st.image(generated_image_url, caption="생성된 선사시대 그림")

                    # 이미지 다운로드 준비
                    response = requests.get(generated_image_url)
                    image_bytes = io.BytesIO(response.content)

                    # 이미지 다운로드 버튼
                    st.download_button(label="이미지 다운로드",
                                       data=image_bytes,
                                       file_name="prehistoric_scene.jpg",
                                       mime="image/jpeg")
            except Exception as e:
                st.error(f"일기와 그림 생성 중 오류가 발생했습니다: {e}")
else:
    st.markdown(f"📝 {selected_era} 시대에 대한 내용을 작성해 주세요.")
