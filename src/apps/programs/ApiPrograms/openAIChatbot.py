import streamlit as st
import openai
from dotenv import load_dotenv

# You should make your own API_KEY from the below link.
# https://platform.openai.com/ai-text-classifier
openai.api_key = st.secrets['api_key']["OpenAI_API_KEY"]

load_dotenv()
completion = openai.Completion()

def ReplyBrain(question, chat_log=None):
	FileLog = open(Tpath_3, "r")
	chat_log_template = FileLog.read()
	FileLog.close()
	if chat_log is None:
		chat_log = chat_log_template
	prompt = f'{chat_log}You : {question}\nJarvis : '
	response = completion.create(model="text-davinci-002",
								prompt=prompt,
								temperature=0.5,
								max_tokens=60,
								top_p=0.3,
								frequency_penalty=0.5,
								presence_penalty=0)
	answer = response.choices[0].text.strip()
	chat_log_template_update = chat_log_template + f"\nYou : {question} \nJarvis : {answer}"
	FileLog = open(Tpath_3, "w")
	FileLog.write(chat_log_template_update)
	FileLog.close()
	return answer
