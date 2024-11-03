import streamlit as st
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def showInstructions():
	st.markdown("""
	### How to get your Spotify Client ID and Secret:
	1. Visit [Spotify Developers](https://developer.spotify.com/).
	2. Sign up for a free account.
	3. Go to the Dashboard and create a new App.
	4. Copy the Client ID and Client Secret from the app's settings.
	5. Enter the Client ID and Client Secret in the input fields below.
	""")
	
	client_id = st.text_input("Enter your Spotify Client ID")
	client_secret = st.text_input("Enter your Spotify Client Secret", type="password")
	
	if st.button("Submit") and client_id and client_secret:
		os.environ["SPOTIPY_CLIENT_ID"] = client_id
		os.environ["SPOTIPY_CLIENT_SECRET"] = client_secret
		st.rerun()

def authenticateSpotify():
	client_id = os.environ.get("SPOTIPY_CLIENT_ID")
	client_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")
	
	if client_id and client_secret:
		auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
		sp = spotipy.Spotify(auth_manager=auth_manager)
		return sp
	return None

def fetchMusicData(sp, search_query, search_type):
	if search_type == 'track':
		results = sp.search(q=search_query, type='track', limit=10)
		return results['tracks']['items']
	elif search_type == 'artist':
		results = sp.search(q=search_query, type='artist', limit=10)
		return results['artists']['items']
	elif search_type == 'album':
		results = sp.search(q=search_query, type='album', limit=10)
		return results['albums']['items']

def displayResults(results, search_type):
	if search_type == 'track':
		for track in results:
			st.image(track["album"]["images"][0]["url"], caption=track["name"], use_column_width=True)
			st.write(f"Artist: {track['artists'][0]['name']}")
			st.write(f"Album: {track['album']['name']}")
			st.write(f"Release Date: {track['album']['release_date']}")
			if track['preview_url']:
				st.write("Preview:")
				st.audio(track['preview_url'])
			else:
				st.write("Preview not available.")
			st.markdown("---")
	elif search_type == 'artist':
		for artist in results:
			if artist["images"]:
				st.image(artist["images"][0]["url"], caption=artist["name"], use_column_width=True)
			st.write(f"Followers: {artist['followers']['total']}")
			st.write(f"Genres: {', '.join(artist['genres'])}")
			st.markdown("---")
	elif search_type == 'album':
		for album in results:
			st.image(album["images"][0]["url"], caption=album["name"], use_column_width=True)
			st.write(f"Artist: {album['artists'][0]['name']}")
			st.write(f"Release Date: {album['release_date']}")
			st.markdown("---")

def music():
	st.title("Play Your Music 🎶")
	if not os.environ.get("SPOTIPY_CLIENT_ID") or not os.environ.get("SPOTIPY_CLIENT_SECRET"):
		showInstructions()
		return
	sp = authenticateSpotify()
	if sp is None:
		st.error("Invalid Spotify Client ID or Secret. Please try again.")
		return

	st.markdown("#### Music Search")
	search_query = st.text_input("Enter artist, album, or track name")
	search_type = st.selectbox("Select search type", ["track", "album", "artist"])
	if st.button("Search") and search_query:
		with st.spinner("Fetching results..."):
			results = fetchMusicData(sp, search_query, search_type)
			displayResults(results, search_type)
