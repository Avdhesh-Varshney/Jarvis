import streamlit as st
import requests
import pickle
import gdown

@st.cache_data
def load_data():
	gdown.download(f"https://drive.google.com/uc?id={st.secrets['movieRecommendationModel']['MOVIES_LIST']}", 'movies_list.pkl', quiet=False)
	gdown.download(f"https://drive.google.com/uc?id={st.secrets['movieRecommendationModel']['SIMILARITY']}", 'similarity.pkl', quiet=False)
	movies_data = pickle.load(open('movies_list.pkl', 'rb'))
	similarity = pickle.load(open('similarity.pkl', 'rb'))
	movies_list = movies_data['title'].values
	return movies_data, similarity, movies_list

try:
	movies_data, similarity, movies_list = load_data()
except Exception as e:
	st.error(f"Data could not be loaded: {e}", icon="🚨")
	st.stop()

def fetchData(movie_id):
	url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={st.secrets['api_key']['TMDB_API_KEY']}"
	data = requests.get(url).json()
	movie_data = {
		'original_title': data['original_title'],
		'poster_path': f"https://image.tmdb.org/t/p/w500{data['poster_path']}",
		'backdrop_path': f"https://image.tmdb.org/t/p/w500{data['backdrop_path']}",
		'overview': data['overview'],
		'runtime': data['runtime'],
		'release_date': data['release_date'],
		'spoken_languages': data['spoken_languages'],
		'genres': data['genres']
	}
	return movie_data

def recommend(movie, num_movies_recommend):
	movie_index = movies_data[movies_data['title'] == movie].index[0]
	distances = similarity[movie_index]
	movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:num_movies_recommend+1]
	recommended_movies = []
	recommended_movies_data = []
	for i in movies_list:
		recommended_movies.append(movies_data.iloc[i[0]].title)
		poster = fetchData(movies_data.iloc[i[0]].id)
		recommended_movies_data.append(poster)
	return recommended_movies, recommended_movies_data

def movieRecommendationModel():
	st.markdown("### Welcome to Movie Recommendation Model")
	movie = st.selectbox("Select a movie from dropdown", [None] + [m for m in movies_list])
	num_movies_recommend = st.slider("Select number of movies to recommend", 1, 10, 4)
	
	if st.button("Show Recommend") and movie is not None:
		recommended_movies, recommended_movies_data = recommend(movie, num_movies_recommend)
		if recommended_movies:
			st.success("Recommended Movies", icon="✅")
			for i, (m, p) in enumerate(zip(recommended_movies, recommended_movies_data)):
				col1, col2 = st.columns(2)
				with col1:
					if p['poster_path']:
						st.image(p['poster_path'], width=350, caption=p['original_title'])
					elif p['backdrop_path']:
						st.image(p['backdrop_path'], width=350, caption=p['original_title'])
					else:
						st.write("Poster not available")
				with col2:
					st.write(f"> ##### {i+1}. {m}")
					st.write(f"**Overview**: {p['overview']}")
					st.write(f"**Runtime**: {p['runtime']} minutes")
					st.write(f"**Release Date**: {p['release_date']}")
					st.write(f"**Spoken Languages**: {', '.join([l['name'] for l in p['spoken_languages']])}")
					st.write(f"**Genres**: {', '.join([g['name'] for g in p['genres']])}")
					st.markdown("---")
		else:
			st.error("No movies found for recommendation.", icon="🚨")
	st.info("This model is based on content-based filtering.", icon="ℹ️")
