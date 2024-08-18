import os
import importlib
import streamlit as st
from src.helpers.getModules import getModules

MAIN_DIR = 'Messenger'
BASE_DIR = os.path.dirname(__file__)
COMMON_MODULE_PATH = os.path.join(BASE_DIR, MAIN_DIR)
MODULES = getModules(COMMON_MODULE_PATH)

def messenger():
  st.title('Messanger Programs')
  choice = st.selectbox('Select a program to execute', [None] + list(MODULES.keys()))
  st.markdown('---')

  if choice in MODULES:
    module_name = MODULES[choice]
    try:
      module = importlib.import_module(f"src.apps.pages.automations.{MAIN_DIR}.{module_name}")
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

messenger()
