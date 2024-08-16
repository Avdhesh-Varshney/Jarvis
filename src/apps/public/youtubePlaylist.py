import streamlit as st
import requests

def API_Exist():
  if st.secrets["YOUTUBE_API_KEY"] != "":
    return True
  return False

def youtubePlaylistVideos(API_KEY, playlist_id):
  url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={playlist_id}&key={API_KEY}"
  response = requests.get(url)
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
    API_KEY = st.secrets["YOUTUBE_API_KEY"]
    playlistId = "PLPUts_2rBVRVTrLlcB54Hwi6Ws51UWLXU"
    videos = youtubePlaylistVideos(API_KEY, playlistId)
    displayVideos(videos)
  else:
    st.error("YouTube API key not found. Please add your API key to the secrets manager.", icon="🚨")

youtubePlaylist()
