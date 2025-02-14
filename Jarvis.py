from database.mongodb import create_connection, login_user
from database.localStorageServer import server
from src.utils.functions import application
from src.utils.emotions import detect_emotion  # Import emotion detection
from datetime import datetime, timedelta
import streamlit as st
import speech_recognition as sr
from streamlit_audio_recorder import st_audio_recorder

if "user" not in st.session_state:
    st.session_state.update({
        'password': None,
        'user': ['', '', '', '', '', '', '', ''],
        'expiration_date': (datetime.now() - timedelta(days=10)).isoformat(),
        'verified': False,
        'emotion': "Neutral"  # Store detected emotion
    })

def get_credentials():
    conn = server()
    return (
        conn.getLocalStorageVal("password"),
        conn.getLocalStorageVal("user"),
        conn.getLocalStorageVal("expiration_date"),
        conn.getLocalStorageVal("verified"),
    )

# Speech to Text & Emotion Detection
def process_audio():
    st.write("🎙️ **Speak now...**")
    audio_bytes = st_audio_recorder()

    if audio_bytes is not None:
        with open("user_voice.wav", "wb") as f:
            f.write(audio_bytes)

        recognizer = sr.Recognizer()
        with sr.AudioFile("user_voice.wav") as source:
            audio = recognizer.record(source)

        try:
            user_input = recognizer.recognize_google(audio)
            st.write(f"🗣️ You said: {user_input}")

            # Detect Emotion
            emotion = detect_emotion("user_voice.wav")
            st.session_state['emotion'] = emotion  # Store emotion in session
            st.success(f"🔍 Detected Emotion: **{emotion}**")

        except sr.UnknownValueError:
            st.warning("🤖 Jarvis: Sorry, I couldn't understand that.")
        except sr.RequestError:
            st.error("🚨 Error: Speech recognition service is unavailable.")

if __name__ == "__main__":
    today = datetime.now()

    if st.session_state['password'] is None:
        st.session_state['password'], st.session_state['user'], st.session_state['expiration_date'], st.session_state['verified'] = get_credentials()

    if st.session_state['expiration_date'] > today.isoformat() and not st.session_state['verified']:
        conn = create_connection()
        if login_user(conn, st.session_state['user'][0], st.session_state['password']):
            st.session_state['verified'] = True
            server().setLocalStorageVal("verified", True)

    st.title("🧠 Jarvis AI - Voice Assistant")

    # 🎤 Speech Input & Emotion Detection
    process_audio()

    # Show the application if user is verified
    application(st.session_state['verified']).run()
