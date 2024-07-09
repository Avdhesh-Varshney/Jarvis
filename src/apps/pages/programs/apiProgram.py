import streamlit as st

def apiPrograms():
  st.title('API Programs')
  choice = st.selectbox('Select a program to execute', [None, "Jokes", "General Facts", "Gemini ChatBot", "Quote of the Day", "Currency Convertor"])
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
  elif choice == "Quote of the Day":
    from src.apps.pages.programs.ApiPrograms.quotes import show_quote
    show_quote()
  elif choice == "Currency Convertor":
    from src.apps.pages.programs.ApiPrograms.currency import convert
    convert()      
  else:
    st.info("Star this project on [GitHub](https://github.com/Avdhesh-Varshney/Jarvis), if you like it!", icon='⭐')

apiPrograms()
