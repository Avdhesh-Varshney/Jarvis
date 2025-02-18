import requests
import streamlit as st

# Groq API details
API_URL = "https://api.groq.com/openai/v1/chat/completions"

def summarize_text(api_key, text):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.3-70b-versatile",  # Specify the model you wish to use
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text}
        ],
        "max_tokens": 150,  # Adjust as needed
        "temperature": 0.7  # Adjust as needed
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        summary = result['choices'][0]['message']['content']
        return summary
    else:
        return f"Error: {response.status_code} - {response.text}"

def main():
    st.title("Text Summarization using Groq API 🚀")
    api_key = st.text_input("Enter your Groq API Key:", type="password")
    user_input = st.text_area("Enter text to summarize (min 50 words):", height=200)

    if st.button("Summarize"):
        if not api_key:
            st.warning("Please enter your Groq API key.")
        elif len(user_input.split()) < 50:
            st.warning("Please enter at least 50 words.")
        else:
            with st.spinner("Summarizing..."):
                summary = summarize_text(api_key, user_input)
                st.subheader("Summary:")
                st.write(summary)

if __name__ == "__main__":
    main()
