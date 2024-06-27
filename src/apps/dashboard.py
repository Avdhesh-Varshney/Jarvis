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
		argon2-cffi==23.1.0
		jupyterlab==4.2.2
		keras==3.4.0
		notebook==7.2.1
		numpy==1.26.4
		pandas==2.2.2
		pillow==10.3.0
		pyttsx3==2.90
		requests==2.31.0
		setuptools==70.1.1
		SpeechRecognition==3.10.3
		streamlit==1.36.0
		tensorflow==2.16.1
	''')

dashboard()
