from requests import get
from json import loads
import streamlit as st

# code files
from src.utils.english import Speak

def fact():
    response = get('https://uselessfacts.jsph.pl/api/v2/facts/random')
    fact = loads(response.text)['text'].title()
    box = st.empty()
    box.markdown(fact)
    Speak(fact)
