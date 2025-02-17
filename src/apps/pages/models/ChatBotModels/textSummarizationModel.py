import streamlit as st
import requests

# Function to call Groq API for summarization
@st.cache_resource(show_spinner=True)

def load_summarizer():
    # Groq API endpoint and headers (replace with actual API details)
    api_url = "https://api.groq.com/summarize"  
    headers = {
        "Authorization": "Bearer YOUR_GROQ_API_KEY",
        "Content-Type": "application/json"
    }
    return api_url, headers

def textSummarizationModel():
    st.subheader("Text Summarization Tool")
    api_url, headers = load_summarizer()

    st.write("Enter the text you'd like to summarize (minimum 50 words).")
    user_input = st.text_area("Input Text", height=200)

    if st.button("Summarize"):
        if len(user_input.split()) < 50:
            st.warning("Please enter at least 50 words for summarization.")
        else:
            with st.spinner("Summarizing..."):
                response = requests.post(api_url, headers=headers, json={"text": user_input})
                if response.status_code == 200:
                    summary = response.json()['summary']
                    st.subheader("Summary:")
                    st.write(summary)
                else:
                    st.error("Error in summarization. Please try again.")
