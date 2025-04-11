import streamlit as st
import pandas as pd
import difflib
import pickle
import time
from fetch_poster import fetch_poster
import os
import gdown

if not os.path.exists("similarity.pkl"):
    file_id = "1AbCdEFGHIjklmn1234"  # Replace with your actual file ID
    url = f"https://drive.google.com/file/d/1MbRi-CuuBxDAu7ybuTO0gcKvfGNluQjO"
    st.info("Downloading similarity matrix...")
    gdown.download(url, "similarity.pkl", quiet=False)

# Load Data
movies = pd.read_csv('movies.csv')
similarity = pickle.load(open('similarity.pkl', 'rb'))

# App Config
st.set_page_config(page_title="Movie Recommender 🎥", layout="centered")
st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Find movies similar to your favorite ones!</h4>", unsafe_allow_html=True)
st.markdown("---")

# User Input
movie_name = st.text_input("🔍 Enter the name of your favorite movie:")

# Recommender Logic
if movie_name:
    with st.spinner('✨ Finding similar movies for you...'):
        time.sleep(1.5)  # Simulate loading

        movie_titles = movies['title'].tolist()
        close_match = difflib.get_close_matches(movie_name, movie_titles)

        if close_match:
            closest_match = close_match[0]
            index_of_movie = movies[movies.title == closest_match]['index'].values[0]

            similarity_score = list(enumerate(similarity[index_of_movie]))
            sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)[1:21]

            st.success(f"✅ Top 15 movies similar to **{closest_match}**:")
            st.markdown("")

            # Display in 4 columns
            cols = st.columns(4)
            for i, movie in enumerate(sorted_similar_movies):
                index = movie[0]
                title = movies.loc[index, 'title']
                poster_url = fetch_poster(title)

                with cols[i % 4]:
                    st.image(poster_url, width=170)
                    st.markdown(f"""
                        <div style='width: 170px; white-space: nowrap; overflow: hidden; color: white;'>
                            <marquee behavior="scroll" direction="left" scrollamount="4" style='font-size:16px; color:#ffffff;'>
                                <b>{i+1}. {title}</b>
                            </marquee>
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
        else:
            st.error("❌ Couldn't find a close match. Try a different movie name!")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 14px;'>
        Developed by <b>Abhay</b> | 🌐 
        <a href='https://github.com/abhay-707/' target='_blank' style='color: #1f77b4; text-decoration: none;'>
            View on GitHub
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
