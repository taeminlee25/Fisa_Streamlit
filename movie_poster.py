import streamlit as st
import requests

# TMDb API 키 설정
API_KEY = st.secrets["tmdb"]["api_key"]

# 영화 제목을 입력받는 텍스트 입력 필드
movie_title = st.text_input("영화 제목을 입력하세요:")

# 영화 제목이 입력되면 API를 호출
if movie_title:
    # TMDb API URL 설정
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"

    # API 호출하여 데이터 받기
    response = requests.get(url)
    data = response.json()
    
    # 영화 포스터 출력
    if data['results']:
        poster_path = data['results'][0]['poster_path']
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        st.image(poster_url, caption=f"영화: {data['results'][0]['title']}", use_container_width=True)
    else:
        st.error("영화를 찾을 수 없습니다.")
