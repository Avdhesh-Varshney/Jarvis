import streamlit as st

def dashboard():
	st.title("Jarvis - A Virtual AI Assistant!")
	st.image('assets/image.gif', caption='Jarvis - A Virtual AI Assistant')

	st.write('''
		Jarvis is a simple Python program that can be used to control your computer using voice commands. The program can perform a variety of tasks, such as opening websites, playing music, searching Wikipedia, getting the time, opening code editors, and sending emails.
	''')

	st.markdown('''
		### The objectives of Jarvis
		- To create a simple Python program.
		- To control a computer using voice commands.
		- Perform a variety of tasks,
			- Opening websites
			- Playing music
			- Searching Wikipedia
			- Getting the time
			- Opening code editors
			- Sending emails, etc.
		### Required Libraries
	''')

	st.code('''
		argon2-cffi
		jupyterlab
		keras
		notebook
		numpy
		pandas
		pillow
		pyttsx3
		requests
		setuptools
		SpeechRecognition
		streamlit
		tensorflow
	''')

dashboard()
