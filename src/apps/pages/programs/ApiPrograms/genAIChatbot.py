import google.generativeai as genai
import os
import streamlit as st
from dotenv import load_dotenv


# Initialization messages in session state to enable history.
if "messages" not in st.session_state:
  st.session_state.messages = []


def API_exists():
  # Check if the API exists. If it does, load it to the environment.
  try:
    load_dotenv(dotenv_path="src/apps/pages/programs/ApiPrograms/secrets/.env")
    return "GOOGLE_API_KEY" in os.environ
  except:
    return False


def instructions_to_set_API():
  # Helps an user get an API key from google.
  if not API_exists():
    st.markdown("ERROR!")
    st.error(body="No API found!", icon=":material/warning:")
    st.markdown("Here's how you can set the API yourself:")
    st.markdown(
        "Create an empty file called ```.env``` in the secrets folder found as ```src/apps/pages/programs/ApiPrograms/secrets```."
    )
    st.markdown(
      "Then, obtain an API key for Gemini 1.5 Flash from [Google](%s) and add that to the ```.env``` file you just created in this format:"
      % "https://ai.google.dev/gemini-api"
    )
    st.markdown("```GOOGLE_API_KEY=the-api-key-you-just-obtained```")
    st.markdown(
      "The chatbot will be usable until you delete that API key from the file or until you have reached the rate limits (if applicable) of the API key ."
    )
    st.markdown("Once you have added the API key to the file, press reload.")
    if st.button("Reload"):
			# Reload in order to show the chatbot page, instead of the page which helps the user get an API key.
      st.rerun()


def init_chatbot():
	# Display the first "Hi! How can I help you today?" message.
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
		# Get chunks of the response from Gemini and write it as a stream.  
    for chunk in response:
      try:
        yield str(chunk.text)
      except ValueError as e:
          st.error("ValueError: You are not allowed to ask that kind of a prompt!")      
        
		# Append response to session state for use in display_history function.
    st.session_state.messages.append({"role": "ai", "content": response.text})


def display_history():
  for message in st.session_state.messages:
      with st.chat_message(message["role"]):
        st.write(message["content"])


def chatBot():
  # Check if API exists. If it does, configure gemini using the api key otherwise give the user instructions to get an api.
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
  # Start chatting!
  if prompt != "" and prompt is not None:
    user_message = st.chat_message("user")
    st.session_state.messages.append({"role": "user", "content": prompt})
    user_message.write(prompt)
    response = generate_response(chat_instance, prompt)
    st.write_stream(response)        


if __name__ == "__main__":
  chatBot()
