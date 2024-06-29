import streamlit as st

def casualPrograms():
  st.title('Casual Programs')
  choice = st.selectbox('Select a program to execute', [None, 'Timer', 'Password Generator'])

  st.markdown('---')

  if choice == 'Timer':
    from src.apps.pages.programs.CasualPrograms.timer import timer
    timer()
  elif choice == 'Password Generator':
    from src.apps.pages.programs.CasualPrograms.password_generator import password_generator_app
    password_generator_app()
  else:
    st.info("Star this project on [GitHub](https://github.com/Avdhesh-Varshney/Jarvis), if you like it!", icon='⭐')

casualPrograms()
