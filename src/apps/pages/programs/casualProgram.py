import streamlit as st

def casualPrograms():
  st.title('Casual Programs')
  choice = st.selectbox('Select a program to execute', [None, 'Timer'])

  st.markdown('---')

  if choice == 'Timer':
    from src.apps.pages.programs.CasualPrograms.timer import timer
    timer()
  
  else:
    st.info("Star this project on [GitHub](https://github.com/Avdhesh-Varshney/Jarvis), if you like it!", icon='⭐')

casualPrograms()
