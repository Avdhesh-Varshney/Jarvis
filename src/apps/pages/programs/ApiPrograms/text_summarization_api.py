import requests
import streamlit as st

# Groq API details
API_URL = "https://api.groq.com/summarize"
API_KEY = "YOUR_GROQ_API_KEY" #Place your API key here

def summarize_text(text):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {"text": text}

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        return response.json().get('summary', "No summary generated.")
    else:
        return "Error: Unable to summarize the text."

def main():
    st.title("Text Summarization API")
    user_input = st.text_area("Enter text (min 50 words):", height=200)

    if st.button("Summarize"):
        if len(user_input.split()) < 50:
            st.warning("Please enter at least 50 words.")
        else:
            with st.spinner("Summarizing..."):
                summary = summarize_text(user_input)
                st.subheader("Summary:")
                st.write(summary)

if __name__ == "__main__":
    main()
