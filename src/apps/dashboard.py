import streamlit as st

def readPackages(filePath):
	try:
		with open(filePath, 'r', encoding='utf-8') as file:
			lines = file.readlines()
			libraries = [line.split('==')[0].strip() for line in lines]
			return libraries
	except FileNotFoundError:
		return ["requirements.txt not found"]

def dashboard():
	st.title("Jarvis - A Virtual AI Assistant!")
	st.image('assets/image.gif', caption='Jarvis - A Virtual AI Assistant')

	st.write('''
		Jarvis is a simple Python program that can be used to control your computer using voice commands. The program can perform a variety of tasks, such as opening websites, playing music, searching Wikipedia, getting the time, opening code editors, and sending emails.
	''')

	st.video('https://youtu.be/kjIH9qo8dX4')

	st.markdown('''### Required Libraries''')
	packages = readPackages('requirements.txt')
	st.write(packages)

dashboard()
