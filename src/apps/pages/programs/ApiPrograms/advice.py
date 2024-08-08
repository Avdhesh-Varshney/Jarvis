import streamlit as st
import requests

from src.utils.english import Speak

def advice():
  res = requests.get("https://api.adviceslip.com/advice").json()
  advice = res['slip']['advice']
  st.write(advice)
  Speak(advice)
