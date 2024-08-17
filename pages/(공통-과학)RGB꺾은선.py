import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Streamlit 앱 제목
st.title("Time-Series RGB Average Calculator")

# 여러 개의 이미지 업로드 위젯
uploaded_files = st.file_uploader("Upload images in time order...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# 리스트에 RGB 평균값 저장
average_rgb_list = []

if uploaded_files:
    for uploaded_file in uploaded_files:
        # 이미지 열기
        image = Image.open(uploaded_file)
        
        # 이미지를 RGB 값으로 변환하고, NumPy 배열로 변환
        image_array = np.array(image)
        
        # 각 채널(R, G, B)의 평균값 계산
        average_rgb = np.mean(image_array, axis=(0, 1))
        
        # 평균 RGB 값을 리스트에 추가
        average_rgb_list.append(average_rgb)
    
    # DataFrame으로 변환
    df = pd.DataFrame(average_rgb_list, columns=['R_avg', 'G_avg', 'B_avg'])
    df['Time'] = range(1, len(uploaded_files) + 1)  # 시간 축 추가 (1, 2, 3, ...)

    # 꺾은선 그래프 그리기
    plt.figure(figsize=(10, 6))
    plt.plot(df['Time'], df['R_avg'], label='Red Average', color='red', marker='o')
    plt.plot(df['Time'], df['G_avg'], label='Green Average', color='green', marker='o')
    plt.plot(df['Time'], df['B_avg'], label='Blue Average', color='blue', marker='o')
    plt.title('RGB Averages Over Time')
    plt.xlabel('Time')
    plt.ylabel('Average Value')
    plt.xticks(df['Time'])
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # 그래프를 Streamlit 앱에 표시
    st.pyplot(plt)
