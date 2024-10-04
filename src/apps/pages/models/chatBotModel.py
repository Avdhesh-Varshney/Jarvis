import os
import importlib
import streamlit as st
from src.helpers.getFolders import getFolders

MAIN_DIR = 'ChatBotModels'
BASE_DIR = os.path.dirname(__file__)
COMMON_MODULE_PATH = os.path.join(BASE_DIR, MAIN_DIR)
MODULES = getFolders(COMMON_MODULE_PATH)

def chatBotModels():
  st.title('Chat Bot Models')
  choice = st.selectbox('Select a model to execute', [None] + list(MODULES.keys()))
  st.markdown('---')

  if choice in MODULES:
    module_name = MODULES[choice]
    file_name = module_name[0].lower() + module_name[1:]
    try:
      module = importlib.import_module(f"src.apps.pages.models.{MAIN_DIR}.{module_name}.{file_name}")
      func = getattr(module, file_name)
      func()
    except ModuleNotFoundError:
      st.error(f"Module '{file_name}.py' could not be found.")
    except AttributeError:
      st.error(f"Function '{file_name}' could not be found in '{file_name}.py'.")
    except Exception as e:
      st.error(f"An error occurred: {e}")
  else:
    st.info("Star this project on [GitHub](https://github.com/Avdhesh-Varshney/Jarvis), if you like it!", icon='⭐')

chatBotModels()
