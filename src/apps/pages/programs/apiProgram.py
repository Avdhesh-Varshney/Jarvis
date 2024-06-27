import streamlit as st

def apiPrograms():
  st.title('API Programs')
  choice = st.selectbox('Select a program to execute', [None, "Jokes"])
  if choice == "Jokes":
    from src.apps.pages.programs.ApiPrograms.Jokes import play_joke
    play_joke()
  st.markdown('---')

apiPrograms()
