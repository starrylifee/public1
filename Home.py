import streamlit as st

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

# 홈 페이지의 타이틀 설정
st.title('초등학생용 인공지능도구 모음 홈페이지')

# 애플리케이션 소개
st.markdown("""
    ## 🌟 안녕하세요!
    이 애플리케이션은 여러 가지 인공지능 도구들을 모아 놓은 곳입니다. 아래는 사용할 수 있는 도구들의 리스트와 각 도구의 간략한 설명입니다.
""")

# 추가적인 정보 제공
st.markdown("""
    ## 🚀 시작하기
    왼쪽의 탐색 바를 사용하여 원하는 도구를 선택하고 사용해 보세요. > 표시를 누르면 인공지능 도구 리스트가 나옵니다.
""")

# 공통
st.subheader('공통')
st.write('인공지능 도구를 체험해보세요.')

# 원중초
st.subheader('원중초')
st.write('원중초등학교 학생들이 보내준 아이디어로 만든 5가지의 인공지능 웹앱입니다.')

# 창도초
st.subheader('창도초')
st.write('창도초등학교 학생들이 보내준 아이디어로 만든 5가지의 인공지능 웹앱입니다.')

# 휘경초
st.subheader('휘경초')
st.write('휘경초등학교 학생들이 보내준 아이디어로 만든 5가지의 인공지능 웹앱입니다.')
