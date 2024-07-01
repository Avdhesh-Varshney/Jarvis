import streamlit as st

def games():
  st.title('Games')
  choice = st.selectbox('Select a Game to execute', [None, "Tic-Tac-Toe"])
  st.markdown('---')
  if choice == "Tic-Tac-Toe":
    from src.apps.pages.programs.Games.tictactoe import tictactoe
    tictactoe()
  else:
    st.info("Star this project on [GitHub](https://github.com/Avdhesh-Varshney/Jarvis), if you like it!", icon='⭐')

games()