import streamlit as st
def camelToReadable(camelCaseName):
  st.markdown('---')
  st.write(f"Original Camel Case Name: {camelCaseName}")
  readableName = ''.join([' ' + char if char.isupper() else char for char in camelCaseName]).strip()
  st.write(f"Readable Name: {readableName}")
  st.write(f"Readable Title Name: {readableName.title()}")
  st.markdown('---')
  return readableName.title()
