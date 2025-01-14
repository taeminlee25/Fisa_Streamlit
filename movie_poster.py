import streamlit as st
import requests

# 페이지 초기 설정
st.set_page_config(layout="wide")

def get_movie_data(movie_name):
    api_key = st.secrets["tmdb"]["api_key"]
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}"
    search_response = requests.get(search_url).json()

    if search_response['results']:
        movie_id = search_response['results'][0]['id']
        details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
        details_response = requests.get(details_url).json()
        return details_response
    return None

def get_reviews(movie_name):
    api_key = st.secrets["tmdb"]["api_key"]
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}"
    search_response = requests.get(search_url).json()

    if search_response['results']:
        movie_id = search_response['results'][0]['id']
        reviews_url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={api_key}"
        reviews_response = requests.get(reviews_url).json()
        return reviews_response.get('results', [])
    return []

st.sidebar.title("Movie Search")
movie_name = st.sidebar.text_input("Enter a movie name:")


if movie_name:
    movie_data = get_movie_data(movie_name)
    reviews = get_reviews(movie_name)

    if movie_data:
        col1, col2 = st.columns(2, border=True)
        col3, col4 = st.columns(2, border=True)

        poster_path = movie_data.get("poster_path")
        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            with col1:
                st.header(movie_data.get("title"))
                st.image(poster_url, width=300)
        
        with col2:
            st.subheader("Plot")
            st.write(movie_data.get("overview"))


        if reviews:
            
            good_reviews = [r for r in reviews if int(r.get('author_details', {}).get('rating', 0)) >= 7]
            
            bad_reviews = [r for r in reviews if int(r.get('author_details', {}).get('rating', 0)) < 7]
            with col3:
                st.markdown("### Good Reviews")
                for review in good_reviews[:3]:
                    st.write(f"**{review['author']}**: {review['content'][:200]}...")
            with col4:
                st.markdown("### Bad Reviews")
                for review in bad_reviews[:3]:
                    st.write(f"**{review['author']}**: {review['content'][:200]}...")
        else:
            st.write("No reviews available.")

    else:
        st.write("Movie not found or data unavailable.")
