import streamlit as st
from PIL import Image
import numpy as np

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

# Streamlit 앱 제목
st.title("이미지분석기")

# 이미지 업로드 위젯
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 이미지 열기
    image = Image.open(uploaded_file)
    
    # 이미지를 화면에 표시
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    # 이미지를 RGB 값으로 변환하고, NumPy 배열로 변환
    image_array = np.array(image)
    
    # 각 채널(R, G, B)의 평균값 계산
    average_rgb = np.mean(image_array, axis=(0, 1))
    
    # 결과 출력
    st.write(f"RGB Average: R={average_rgb[0]:.2f}, G={average_rgb[1]:.2f}, B={average_rgb[2]:.2f}")
