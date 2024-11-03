import streamlit as st
import requests

from src.utils.english import Speak

def showAdvice():
	res = requests.get("https://api.adviceslip.com/advice").json()
	advice_text = res['slip']['advice']
	st.write("### Here's your piece of advice:")
	st.markdown(f"> **{advice_text}**")
	Speak(advice_text)

def advice():
	st.title("💡 Jarvis Advice Generator")

	st.markdown(
	"""
	Welcome to the Jarvis Advice Generator! 
	Click the button below to receive a random piece of advice.
	"""
	)

	if st.button("Get Advice"):
		showAdvice()
