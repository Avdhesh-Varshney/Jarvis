import streamlit as st
import requests
import os

BASE_URL = "https://api.themoviedb.org/3"
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"

if 'page' not in st.session_state:
	st.session_state.page = 1

def API_Exists():
	if "TMDB_API_KEY" in st.secrets['api_key'] and st.secrets['api_key']["TMDB_API_KEY"]:
		return True
	elif "TMDB_API_KEY" in os.environ and os.environ["TMDB_API_KEY"]:
		return True
	return False

def showInstructions():
	st.markdown("""### How to get your API Key:
	1. Visit [themoviedb.org](https://www.themoviedb.org/).
	2. Sign up for a free account.
	3. Generate an API key from your account dashboard.
	4. Enter the API key in the input field.
	""")
	api_key = st.text_input("Enter your themoviedb.org API Key")
	if st.button("Enter") and api_key != "":
		os.environ["TMDB_API_KEY"] = api_key
		st.rerun()

def fetchTrendingMovies(TMDB_API_KEY, page):
	response = requests.get(f"{BASE_URL}/trending/movie/day?api_key={TMDB_API_KEY}&page={page}").json()
	return response['results']

def trendingMovies(TMDB_API_KEY):
	st.markdown("#### Trending Movies")
	
	response = requests.get(f"{BASE_URL}/genre/movie/list?api_key={TMDB_API_KEY}").json()
	genres = {genre['id']: genre['name'] for genre in response['genres']}
	current_page = st.session_state.page
	results = fetchTrendingMovies(TMDB_API_KEY, current_page)
	
	for movie in results:
		st.image(f"{POSTER_BASE_URL}/{movie['backdrop_path']}", caption=movie["title"], use_column_width=True)
		st.write(movie["overview"])

		col1, col2 = st.columns(2)
		with col1:
			st.write("Vote Count: ", movie["vote_count"])
			st.write("Rating: ", movie["vote_average"])
			st.write("Popularity: ", movie["popularity"])
			st.write("Adult: ", movie["adult"])
			st.write("Video: ", movie["video"])
		with col2:
			st.write("Original Title: ", movie["original_title"])
			st.write("Release Date: ", movie["release_date"])
			st.write("Original Language: ", movie["original_language"])
			st.write("Media Type: ", movie["media_type"])
			genre_names = [genres[genre_id] for genre_id in movie["genre_ids"]]
			st.write("Genre: ", ", ".join(genre_names))
		st.markdown("---")

	cola, colb, colc, cold = st.columns(4)
	with cola:
		if st.button("Previous Page") and st.session_state.page > 1:
			st.session_state.page -= 1
			st.rerun()
	with cold:
		if st.button("Next Page"):
			st.session_state.page += 1
			st.rerun()

def movies():
	st.title("Watch Your Movies")

	if not API_Exists():
		showInstructions()
		return
	
	TMDB_API_KEY = (os.environ.get("TMDB_API_KEY") or st.secrets['api_key']["TMDB_API_KEY"])
	choice = st.selectbox("Select an option", [None, "Trending Movies"])
	if choice == "Trending Movies":
		trendingMovies(TMDB_API_KEY)
	else:
		st.warning("Please select an option from the dropdown menu.", icon="🚨")
