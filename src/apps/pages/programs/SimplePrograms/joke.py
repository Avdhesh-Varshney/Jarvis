from requests import get
from json import loads
import streamlit as st

# code files
from src.utils.english import Speak

def joke():
    response = get('https://official-joke-api.appspot.com/random_joke')
    joke_question = loads(response.text)['setup'].title()
    joke_response = loads(response.text)['punchline'].title()
    box = st.empty()
    text = joke_question
    box.code(text,language=None)
    Speak(joke_question)
    text += '\n'+joke_response
    box.code(text,language=None)
    Speak(joke_response)
    text += '\n😂😂'
    box.code(text,language=None)
