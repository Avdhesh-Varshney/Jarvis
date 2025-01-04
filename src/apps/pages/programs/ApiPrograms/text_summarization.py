import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import json

# Function to check if the Groq API key exists
def API_Exists():
    """
    Check if Groq API key exists in Streamlit secrets or environment variables.

    Returns:
        bool: True if the API key exists, otherwise False.
    """
    if "GROQ_API_KEY" in st.secrets["api_key"] and st.secrets["api_key"]["GROQ_API_KEY"]:
        return True
    elif "GROQ_API_KEY" in os.environ and os.environ["GROQ_API_KEY"]:
        return True
    return False

# Streamlit app
def text_summarization():
    st.title("Text Summarization using Groq")
    st.markdown("Enter text to generate a concise summary using the Groq LLM.")

    # Check if API key exists
    if not API_Exists():
        st.error("Groq API key is missing. Please add it to Streamlit secrets or environment variables.")
        return

    # Retrieve the API key
    GROQ_API_KEY = st.secrets["api_key"].get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY"))

    # Initialize the Groq LLM
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        api_key=GROQ_API_KEY,
        temperature=0.7
    )

    # Define the summarization prompt
    summarization_prompt = ChatPromptTemplate.from_messages([
        ("system", """Summarize the given text into a concise and coherent paragraph.
        Return the summary in the following JSON format:
        {{
            "summary": "your summary here"
        }}
        """),
        ("user", "{input}")
    ])

    # Define a JSON output parser
    parser = JsonOutputParser(pydantic_object={
        "type": "object",
        "properties": {
            "summary": {"type": "string"}
        }
    })

    # Create the summarization chain
    chain = summarization_prompt | llm | parser

    # Input text for summarization
    input_text = st.text_area("Enter Text to Summarize", placeholder="Paste your text here...")

    if st.button("Generate Summary"):
        if not input_text.strip():
            st.warning("Please enter some text to summarize.")
        else:
            try:
                # Summarize the text
                result = chain.invoke({"input": input_text})
                st.success("Summary Generated!")
                st.json(result)
            except Exception as e:
                st.error(f"Error during summarization: {e}")