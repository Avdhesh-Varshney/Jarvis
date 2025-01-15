import streamlit as st
from src.emotion_recognition import run_emotion_detection

st.title("Emotion Recognition with Jarvis")
st.write("Click the button to start emotion detection.")

if st.button('Start Emotion Recognition'):
    run_emotion_detection()
