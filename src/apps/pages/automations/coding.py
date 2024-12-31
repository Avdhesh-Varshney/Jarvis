import os
import importlib
import streamlit as st
from src.helpers.getModules import getModules

# Constants
MAIN_DIR = 'Coding'
BASE_DIR = os.path.dirname(__file__)
COMMON_MODULE_PATH = os.path.join(BASE_DIR, MAIN_DIR)
MODULES = getModules(COMMON_MODULE_PATH)

def load_and_execute_module(module_name):
    """Loads and executes the specified module."""
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

def coding():
    """Main function to display coding platforms and execute selected program."""
    st.title('Coding Platforms')
    choice = st.selectbox('Select a program to execute', [None] + list(MODULES.keys()))
    st.markdown('---')

    if choice:
        load_and_execute_module(MODULES[choice])
    else:
        st.info("Star this project on [GitHub](https://github.com/Avdhesh-Varshney/Jarvis), if you like it!", icon='⭐')

if __name__ == "__main__":
    coding()
