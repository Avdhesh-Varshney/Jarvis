import streamlit as st

def apiPrograms():
  st.title('API Programs')
  choice = st.selectbox('Select a program to execute', [None, "Jokes", "General Facts", "Gemini ChatBot", "World Clock"])
  st.markdown('---')
  if choice == "Jokes":
    from src.apps.pages.programs.ApiPrograms.joke import play_joke
    play_joke()
  elif choice == "General Facts":
    from src.apps.pages.programs.ApiPrograms.fact import play_fact
    play_fact()
  elif choice == "Gemini ChatBot":
    from src.apps.pages.programs.ApiPrograms.genAIChatbot import chatBot
    chatBot()
  elif choice == "World Clock":
    from src.apps.pages.programs.ApiPrograms.worldClock import display_world_clock
    display_world_clock()
  else:
    st.info("Star this project on [GitHub](https://github.com/Avdhesh-Varshney/Jarvis), if you like it!", icon='⭐')

apiPrograms()
