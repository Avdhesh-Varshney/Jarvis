import streamlit as st

def simplePrograms():
  st.title('Simple Programs')
  choice = st.selectbox('Select a program to execute', [None, 'Timer', 'Password Generator','Caeser Cipher', 'Calculator', 'World Clock'])

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
  elif choice == 'Calculator':
    from src.apps.pages.programs.SimplePrograms.calculator import calculator
    calculator()
  elif choice == 'World Clock':
    from src.apps.pages.programs.SimplePrograms.worldClock import display_world_clock
    display_world_clock()
  else:
    st.info("Star this project on [GitHub](https://github.com/Avdhesh-Varshney/Jarvis), if you like it!", icon='⭐')

simplePrograms()
