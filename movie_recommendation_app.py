import streamlit as st
import pickle
import pandas as pd
import requests
import compress_pickle

#Function to fetch  image poster from tmdb api
def fetch_posters(movie_id):
    """
    Input: Taken in movie_id. It is of type integer
    Output: Poster path corresponding to the movie id fetched from the tmdb API
    """

    #This fetches the url of the movie corresponding to the movie id from tmdb api
    url = 'https://api.themoviedb.org/3/movie/{}?language=en-US'.format(movie_id)

    headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2ZWIxYjMzMmE0ZGI3YWE4YTMxZTQ0OTJhN2JmZjg3YSIsInN1YiI6IjY0ZDE1ZDFmZDhkMzI5MDBlNDBjNjJkMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.vKEWQ6F6Hu-IByFksMKMU7FYch0RsMoAy_W5fc5k1HE"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return "https://image.tmdb.org/t/p/original/"+data['poster_path']


def recommend(movie):
     #Get the index of the movie
    movie_idx = movies[movies['title'] == movie].index[0]
    #Find the similarity row corresponding to that movie
    distances = similarity[movie_idx]
    #Sort the distances and get the top 5 movie index that is similar to our queried movie
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]
    recommend_list = []
    recommend_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommend_list.append(movies.iloc[i[0]].title)
        recommend_movie_posters.append(fetch_posters(movie_id))
    return recommend_list, recommend_movie_posters
        
movie_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movie_dict)
#similarity = pickle.load(open('similarity.pkl','rb'))
similarity = compress_pickle.load(open('compressed_similarity.pkl','rb'), compression="gzip")
st.title("Movie Recommender System")
selected_moviename = st.selectbox('Search for movies', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_moviename)
    col1, col2, col3, col4, col5 = st.columns(5, gap = "medium")
    with col1:
        st.write("##### "+names[0])
        st.image(posters[0])
    with col2:
        st.write("##### "+names[1])
        st.image(posters[1])
    with col3:
        st.write("##### "+names[2])
        st.image(posters[2])
    with col4:
        st.write("##### "+names[3])
        st.image(posters[3])
    with col5:
        st.write("##### "+names[4])
        st.image(posters[4])