import pickle
import streamlit as st
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=5d667a520db94535ac0a5c06a12a21d3&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    matches = movies[movies['title'] == movie]
    if matches.empty:
        st.error(f"No movie found with title: {movie}")
        return [], []

    index = matches.index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# ------------------ UI ------------------
st.header('🎬 Movie Recommender System')

# Load data
movies = pd.DataFrame(pickle.load(open('model/movie_dict.pkl','rb')))
similarity = pickle.load(open('model/similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    if recommended_movie_names:  # only if we got results
        cols = st.columns(5)
        for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
            with col:
                st.text(name)
                st.image(poster)
