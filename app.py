import pickle
import streamlit as st
import requests

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster: {e}")  # <-- helpful log
        return "https://via.placeholder.com/500x750?text=Error"



# Function to recommend movies
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)
        return recommended_movie_names, recommended_movie_posters
    except IndexError:
        return [], []

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #f5f5f5;
        font-family: Arial, sans-serif;
    }
    .stButton>button {
        background-color: #ECEFCA; /* Remove background color */
        color: black; /* Default text color */
        border: 1px solid #ccc; /* Add a subtle border */
        border-radius: 5px;
        padding: 10px 20px;
        margin: 0 auto; /* Center the button */
        display: block; /* Ensure the button is treated as a block element */
    }
    .stButton>button:hover {
        background-color: #f0f0f0; /* Add a light hover effect */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>🎥 Movie Recommender System 🎥</h1>",
    unsafe_allow_html=True
)

# Load data
movies = pickle.load(open('artificats/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artificats/similarity.pkl', 'rb'))

# Dropdown for movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list,
    placeholder="Select a movie to get recommendations"
)

# Button to show recommendations
if st.button('Show Recommendation'):
    if selected_movie:
        with st.spinner('Fetching recommendations...'):
            recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        if recommended_movie_names:
            st.markdown("<h3 style='text-align: center;'>Recommended Movies</h3>", unsafe_allow_html=True)
            cols = st.columns(len(recommended_movie_names))
            for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
                with col:
                    st.image(poster, use_container_width=True)
                    st.markdown(f"<p style='text-align: center;'>{name}</p>", unsafe_allow_html=True)
        else:
            st.error("No recommendations found. Please try another movie.")
    else:
        st.warning("Please select a movie before clicking the button.")

# Footer
st.markdown(
    """
    <hr>
    <p style='text-align: center; font-size: 14px; color: gray;'>
    Made with ❤️ using Streamlit | © 2025 Movie Recommender
    </p>
    """,
    unsafe_allow_html=True
)