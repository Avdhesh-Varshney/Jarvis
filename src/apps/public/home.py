import streamlit as st

# Initialize session state to track video playback
if 'video_played' not in st.session_state:
    st.session_state.video_played = False

# Function to show the intro video if it hasn't been played yet
def show_intro_video():
    st.markdown(
        """
        <style>
        .video-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 9999;
            background: black;
        }
        </style>
        <div class="video-container" id="video-container">
            <video id="intro-video" autoplay muted playsinline style="width: 100%; height: 100%;">
                <source src="src/intro.mp4" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </div>
        <script>
            const video = document.getElementById('intro-video');
            const container = document.getElementById('video-container');
            video.onended = function() {
                container.style.display = 'none';
                fetch('/?video_played=true');  // Make a request to update session state
            };
        </script>
        """,
        unsafe_allow_html=True
    )

# Display the home page with app details
def home():
    st.title("Welcome to Jarvis - Your Virtual AI Assistant!")
    st.image('assets/image.gif', caption='Empower Your Digital Life with Jarvis', use_column_width=True)
    
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

    st.markdown("## See Jarvis in Action")
    st.video('https://youtu.be/kjIH9qo8dX4')

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

# Main function to control which content displays
def main():
    if st.session_state.video_played:
        home()
    else:
        show_intro_video()

# Run the main function
main()
