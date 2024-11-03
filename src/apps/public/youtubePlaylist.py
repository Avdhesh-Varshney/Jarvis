import streamlit as st
import requests
import os

URL="https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId=PLPUts_2rBVRVTrLlcB54Hwi6Ws51UWLXU"
BLOG_URL="https://avdhesh-portfolio.netlify.app/blog/fetch-youtube-playlist-in-reactjs"

def API_Exist():
	if "YOUTUBE_API_KEY" in st.secrets['api_key'] and st.secrets["api_key"]["YOUTUBE_API_KEY"]:
		return True
	elif "YOUTUBE_API_KEY" in os.environ and os.environ["YOUTUBE_API_KEY"]:
		return True
	return False

def showInstructions():
	st.markdown("### Instructions:")
	st.markdown("""
	1. Go to the [Google Developers Console](https://console.developers.google.com/).
	2. Create a new project or select an existing project.
	3. In the left sidebar, click on 'Credentials'.
	4. Click on 'Create Credentials' and select 'API key'.
	5. Copy the generated API key and paste it in the text box below.
	6. Click on 'Submit' to save the API key.
	""")
	api_key = st.text_input("Enter your YouTube API key")
	if st.button("Submit") and api_key != "":
		os.environ["YOUTUBE_API_KEY"] = api_key
		st.rerun()

def youtubePlaylistVideos(API_KEY):
	URL2 = f"{URL}&key={API_KEY}"
	response = requests.get(URL2)
	videos = response.json().get('items', [])
	return videos

def displayVideos(videos):
	for i in range(0, len(videos), 2):
		cols = st.columns(2)
		for j in range(2):
			if i + j < len(videos):
				video = videos[i + j]
				video_title = video['snippet']['title'].split('|')[0].strip()
				video_url = f"https://www.youtube.com/watch?v={video['snippet']['resourceId']['videoId']}"
				with cols[j]:
					st.markdown(f"##### [{video_title}]({video_url})")
					st.video(video_url)

def youtubePlaylist():
	st.title("🎬 YouTube Playlist")
	st.markdown("Explore the latest videos from the Jarvis YouTube playlist. Watch tutorials, feature demonstrations, and more to get started with Jarvis.")

	if API_Exist():
		API_KEY = (st.secrets['api_key']["YOUTUBE_API_KEY"] or os.environ["YOUTUBE_API_KEY"])
		if st.button("Show Videos"):
			videos = youtubePlaylistVideos(API_KEY)
			displayVideos(videos)
	else:
		showInstructions()
		st.info(f"You can also go through my [blog post]({BLOG_URL}) for a detailed guide on how to get the YouTube API key.", icon="📝")
		st.error("YouTube API key not found. Please add your API key to the secrets manager.", icon="🚨")
