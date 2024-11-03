import streamlit as st

def readPackages(filePath):
	try:
		with open(filePath, 'r', encoding='utf-8') as file:
			lines = file.readlines()
			libraries = [line.split('==')[0].strip() for line in lines]
			return libraries
	except FileNotFoundError:
		return ["requirements.txt not found"]

def packageUsed():
  st.title("Package Used")
  packages = readPackages('requirements.txt')
  st.write(packages)
