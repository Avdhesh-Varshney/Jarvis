import streamlit as st
from database.mongodb import show_data

def userData():
  st.title("📦 User Data")
  data = show_data()
  st.dataframe(data)

userData()
