import streamlit as st
from pydictionary import Dictionary

# TODO: Implement the dictionary function which will take a word as input and display the meaning, synonym and antonym of the word.
def dictionary():
	st.write("Tell Me The Problem!")
	word = st.text_input("Enter the Word")
	if word:
		result = Dictionary(word)
		choice = st.radio("Choose an Option", ['Meaning', 'Synonym', 'Antonym'])
		match(choice):
			case 'Meaning':
				result = result['Noun']
				st.write(f"The Meaning for {word} is {result}")
			case 'Synonym':
				st.write(f"The Synonym for {word} is {result}")
			case 'Antonym':
				st.write(f"The Antonym for {word} is {result}")
	else:
		st.info("Enter a word to continue...", icon="📝")
