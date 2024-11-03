import streamlit as st

def home():
	st.title("Welcome to Jarvis - Your Virtual AI Assistant!")
	st.toast("Welcome to Jarvis!", icon="👋")
	st.video('assets/video.mp4', loop=True, autoplay=True, muted=True)

	st.markdown("""
	## What is Jarvis?
	**Jarvis** is a powerful Python-based AI assistant designed to streamline your daily tasks through simple voice commands. Whether you're navigating the web, managing your media, or automating routine processes, Jarvis is here to help.
	""")

	st.markdown("""
	## Key Features
	- **Voice Commands**: Control your computer effortlessly using voice commands.
	- **Web Automation**: Open websites, search the internet, and get instant results.
	- **Media Control**: Play your favorite music and videos with a single command.
	- **Productivity Tools**: Open code editors, manage your time, and stay organized.
	- **Information Retrieval**: Get instant answers from Wikipedia and other sources.
	- **Email Management**: Send and receive emails directly from the assistant.
	""")

	with st.expander("## See Jarvis in Action"):
		st.video(f'https://www.youtube.com/watch?v={st.secrets["general"]["YOUTUBE_VIDEO_ID"]}', start_time=0)

	st.markdown("""
	## Learn More and Get Started
	Explore the capabilities of Jarvis by diving into the following resources:
	- [Documentation](https://codingblogs.hashnode.dev/) - Comprehensive guides on setting up and using Jarvis.
	- [Community Forums](https://discord.gg/tSqtvHUJzE) - Join discussions with other Jarvis users.
	- [GitHub Repository](https://github.com/Avdhesh-Varshney/Jarvis) - Contribute to the development or get the latest version.
	- [YouTube Playlist](https://www.youtube.com/playlist?list=PLPUts_2rBVRVTrLlcB54Hwi6Ws51UWLXU) - Watch tutorials and feature demonstrations.
	""")

	st.markdown("""
	---
	**Jarvis** is continually evolving with new features and improvements. Stay tuned for updates and feel free to contribute to its development.
	""")
