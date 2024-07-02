import streamlit as st

def simplePrograms():
  st.title('Simple Programs')
  choice = st.selectbox('Select a program to execute', [None, 'Timer', 'Password Generator','Caeser Cipher'])

  st.markdown('---')

  if choice == 'Timer':
    from src.apps.pages.programs.SimplePrograms.timer import timer
    timer()
  elif choice == 'Password Generator':
    from src.apps.pages.programs.SimplePrograms.passwordGenerator import passwordGeneratorApp
    passwordGeneratorApp()
  elif choice == 'Caeser Cipher':
    from src.apps.pages.programs.SimplePrograms.CaeserCipher import caeserCipher
    caeserCipher()
  else:
    st.info("Star this project on [GitHub](https://github.com/Avdhesh-Varshney/Jarvis), if you like it!", icon='⭐')

simplePrograms()
