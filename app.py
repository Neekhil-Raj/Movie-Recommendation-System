<<<<<<< HEAD
import streamlit as st
import pickle
st.title('MRS')
import requests
from concurrent.futures import ThreadPoolExecutor


movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))


def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        params = {
            "api_key": 'ae953c55f96e8955ae9d7c7716ca6bf9',
            "language": "en-US"
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
        else:
            return None

    except requests.exceptions.RequestException as e:
        print("Error fetching poster:", e)
        return None


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
    
    #print(movie_ids)

    #print(movie_names)

    print(movie_posters)

    return movie_names, movie_posters

selected_movies_name = st.selectbox(
    'Select a movie',
    movies['title'].values
)


if st.button('Recommend'):
    names, posters = recommend(selected_movies_name)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(names[i])
            print(names[i])
            if posters[i]:
                st.image(posters[i])
                print(posters[i])
            else:
=======
import streamlit as st
import pickle
st.title('MRS')
import requests
from concurrent.futures import ThreadPoolExecutor


movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))


def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        params = {
            "api_key": 'ae953c55f96e8955ae9d7c7716ca6bf9',
            "language": "en-US"
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
        else:
            return None

    except requests.exceptions.RequestException as e:
        print("Error fetching poster:", e)
        return None


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
    
    #print(movie_ids)

    #print(movie_names)

    print(movie_posters)

    return movie_names, movie_posters

selected_movies_name = st.selectbox(
    'Select a movie',
    movies['title'].values
)


if st.button('Recommend'):
    names, posters = recommend(selected_movies_name)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(names[i])
            print(names[i])
            if posters[i]:
                st.image(posters[i])
                print(posters[i])
            else:
>>>>>>> edcf93c921109d175ab41b9036048d9ba3bb0b82
                st.write("Poster not available")