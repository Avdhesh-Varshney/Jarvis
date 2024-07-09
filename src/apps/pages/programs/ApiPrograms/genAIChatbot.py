import google.generativeai as genai
import os
import streamlit as st

if "messages" not in st.session_state:
  st.session_state.messages = []

def API_exists():
  if os.environ.get("GOOGLE_API_KEY") != "":
    return "GOOGLE_API_KEY" in os.environ
  return False

def set_API():
  st.markdown("Obtain an API key from [Google](%s) and enter it here:" % "https://ai.google.dev/gemini-api")
  API = st.text_input(label="API Key")
  if API != "":
    os.environ["GOOGLE_API_KEY"] = API

def instructions_to_set_API():
  set_API()
  if st.button("Enter"):
    st.rerun()

def init_chatbot():
  if API_exists():
    msg = st.chat_message("ai")
    st.write("Hi! How can I help you today?")


def gemini_init():
  model = genai.GenerativeModel("gemini-1.5-flash")
  chat = model.start_chat(history=[])
  return chat

def generate_response(chat_instance: genai.ChatSession, prompt: str):
  with st.chat_message("ai"):
    response = chat_instance.send_message(prompt, stream=True)
    for chunk in response:
      try:
        yield str(chunk.text)
      except ValueError as e:
        st.error("ValueError: You are not allowed to ask that kind of a prompt!")
        
  st.session_state.messages.append({"role": "ai", "content": response.text})

def display_history():
  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.write(message["content"])

def chatBot():
  if API_exists():
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=GOOGLE_API_KEY)
    prompt = st.chat_input("Let's chat!")
  else:
    instructions_to_set_API()
    prompt = None

  init_chatbot()
  chat_instance = gemini_init()
  display_history()

  if prompt != "" and prompt is not None:
    user_message = st.chat_message("user")
    st.session_state.messages.append({"role": "user", "content": prompt})
    user_message.write(prompt)
    response = generate_response(chat_instance, prompt)
    st.write_stream(response)        
