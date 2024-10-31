import streamlit as st


# Set up session state to track if the intro video has been shown
if 'video_shown' not in st.session_state:
    st.session_state.video_shown = False

def show_intro_video():
    # Display the intro video
    st.image("assets/intro.gif")
    


    # Update session state
    st.session_state.video_shown = True  # Set to True to show the main content next

def home():
    # Main content after video
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

def main():
    if not st.session_state.video_shown:
        show_intro_video()  # Show video if it hasn't been watched
        # Display continue button after video
        if st.button("Continue to App"):
            st.session_state.video_shown = True  # Set to True to show main content next
    else:
        home()  # Show main content after video is "watched"

if __name__ == "__main__":
    main()
