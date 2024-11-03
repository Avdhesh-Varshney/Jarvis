import streamlit as st
import wikipedia

def wikipediaApp():
	st.title("Wikipedia Search")
	query = st.text_input("Enter Your Query: ")
	if st.button("Search") and query != "":
		try:
			line = wikipedia.page("india")
			st.markdown("##### According To Wikipedia")
			st.write(line)
		except:
			st.info(f"Sorry, {query} is not found in Wikipedia. Please try another query.", icon="🚨")
