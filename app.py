import streamlit as st
import pickle
import requests
import time
import os
import gdown
from concurrent.futures import ThreadPoolExecutor

st.title('Movie Recommendation System')

# ===============================
# 📥 DOWNLOAD LARGE FILES (Render)
# ===============================

MOVIES_FILE = "movies.pkl"
SIMILARITY_FILE = "similarity.pkl"

MOVIES_FILE_ID = "PASTE_MOVIES_FILE_ID_HERE"
SIMILARITY_FILE_ID = "PASTE_SIMILARITY_FILE_ID_HERE"

MOVIES_URL = f"https://drive.google.com/uc?id=1xCdoDc41TA8hpmJC-FSlhIzEZ-CFCX8q"
SIMILARITY_URL = f"https://drive.google.com/uc?id=1t6sHdlpgyOtYaiEu17WY8idVEXsrEZMf"

if not os.path.exists(MOVIES_FILE):
    st.info("Downloading movies data...")
    gdown.download(MOVIES_URL, MOVIES_FILE, quiet=False)

if not os.path.exists(SIMILARITY_FILE):
    st.info("Downloading similarity matrix...")
    gdown.download(SIMILARITY_URL, SIMILARITY_FILE, quiet=False)

# ===============================
# 📦 LOAD DATA
# ===============================

movies = pickle.load(open(MOVIES_FILE, 'rb'))
similarity = pickle.load(open(SIMILARITY_FILE, 'rb'))

# ===============================
# 🎬 POSTER FETCH FUNCTION
# ===============================

def fetch_poster(movie_id, delay=0.8):
    try:
        time.sleep(delay)

        url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        params = {
            "api_key": "66a1420a7fb13e7615d4d76997ec22b1",
            "language": "en-US"
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
        return None

    except requests.exceptions.RequestException as e:
        print("Error fetching poster:", e)
        return None

# ===============================
# 🤖 RECOMMENDATION LOGIC
# ===============================

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    movie_ids = [movies.iloc[i[0]].movie_id for i in movies_list]
    movie_names = [movies.iloc[i[0]].title for i in movies_list]

    with ThreadPoolExecutor(max_workers=5) as executor:
        movie_posters = list(executor.map(fetch_poster, movie_ids))

    return movie_names, movie_posters

# ===============================
# 🎯 STREAMLIT UI
# ===============================

selected_movies_name = st.selectbox(
    'Select your favorite movie and get 5 best movie recommendations',
    [''] + movies['title'].tolist()
)

if st.button('Recommend'):
    names, posters = recommend(selected_movies_name)

    progress_bar = st.progress(0)
    status_text = st.empty()

    cols = st.columns(5)
    total = len(names)

    for i in range(total):
        progress = int(((i + 1) / total) * 100)
        progress_bar.progress(progress)
        status_text.text(f"Loading poster {i + 1} of {total}...")

        with cols[i]:
            st.text(names[i])
            time.sleep(0.7)

            if posters[i]:
                st.image(posters[i])
            else:
                st.write("Poster not available")

    status_text.text("✅ Recommendations loaded successfully!")