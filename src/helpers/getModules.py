import os
import streamlit as st
from src.helpers.camelToReadable import camelToReadable

def getModules(COMMON_MODULE_PATH):
  try:
    files = [f for f in os.listdir(COMMON_MODULE_PATH) if f.endswith('.py') and not f.startswith('__')]
  except FileNotFoundError:
    st.error("The specified directory does not exist.")
    return {}
  
  st.write("Files => ", files)
  
  modules = {}
  for file in files:
    module_name = file[:-3]
    readable_name = camelToReadable(module_name)
    st.write("Module Name => ", module_name)
    st.write("Readable Name => ", readable_name)
    modules[readable_name] = module_name
  return modules
