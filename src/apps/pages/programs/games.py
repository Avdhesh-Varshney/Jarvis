import os
import importlib
import streamlit as st
from src.helpers.getModules import getModules

BASE_DIR = os.path.dirname(__file__)
COMMON_MODULE_PATH = os.path.join(BASE_DIR, 'Games')
MODULES = getModules(COMMON_MODULE_PATH)

# debugging
st.write("Base Directory => ", BASE_DIR)
st.write("Common Module Path => ", COMMON_MODULE_PATH)
st.write("Modules => ", MODULES)

def games():
  st.title('🎮 Games 🕹️')

  choice = st.selectbox('Select a program to execute', [None] + list(MODULES.keys()))
  module_name = MODULES[choice]
  st.write("Choice => ", choice)
  st.write("Module Name => ", module_name)
  
  st.markdown('---')

  if choice in MODULES:
    try:
      module = importlib.import_module(f"src.apps.pages.programs.Games.{module_name}")
      st.write("Module => ", module)
      func = getattr(module, module_name)
      func()
    except ModuleNotFoundError:
      st.error(f"Module '{module_name}.py' could not be found.")
    except AttributeError:
      st.error(f"Function '{module_name}' could not be found in '{module_name}.py'.")
    except Exception as e:
      st.error(f"An error occurred: {e}")
  else:
    st.info("Star this project on [GitHub](https://github.com/Avdhesh-Varshney/Jarvis), if you like it!", icon='⭐')

games()
