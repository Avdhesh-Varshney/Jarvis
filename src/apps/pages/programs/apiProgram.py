import streamlit as st

def apiPrograms():
  st.title('API Programs')
  choice = st.selectbox('Select a program to execute', [None, "Jokes"])
  st.markdown('---')
  if choice == "Jokes":
    from src.apps.pages.programs.ApiPrograms.joke import play_joke
    play_joke()
  else:
    st.info("Star this project on [GitHub](https://github.com/Avdhesh-Varshney/Jarvis), if you like it!", icon='⭐')

apiPrograms()
