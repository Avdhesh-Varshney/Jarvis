import streamlit as st
from transformers import pipeline

@st.cache_resource(show_spinner=True)
def load_summarizer():
	return pipeline("summarization", model="t5-small")

def textSummarizationModel():
	st.title("Text Summarization Tool")
	summarizer = load_summarizer()

	st.write("Enter the text you'd like to summarize (minimum 50 words).")
	user_input = st.text_area("Input Text", height=200)

	if st.button("Summarize"):
		if len(user_input.split()) < 50:
			st.warning("Please enter at least 50 words for summarization.")
		else:
			with st.spinner("Summarizing..."):
				summary = summarizer(user_input, max_length=150, min_length=30, do_sample=False)
				st.subheader("Summary:")
				st.write(summary[0]['summary_text'])
