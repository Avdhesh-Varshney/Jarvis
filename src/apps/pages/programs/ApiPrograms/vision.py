import streamlit as st
import google.generativeai as genai
import base64
import os


def validate_file_size(file):
    return file is not None and file.size <= 20 * 1024 * 1024

def show_instructions():
    st.markdown("### Welcome to Vision 🌟")
    st.markdown(
        "To get started, obtain an API key from [Google Gemini API](https://ai.google.dev/gemini-api) and enter it below:")
    api_key = st.text_input("Enter your Google Gemini API Key", type="password")
    if st.button("Submit") and api_key:
        os.environ["GEMINI_API_KEY"] = api_key
        st.success("API Key has been set. Please reload the page.")
        st.rerun()

def api_exists():
    if "GEMINI_API_KEY" in st.secrets['api_key'] and st.secrets['api_key']["GEMINI_API_KEY"]:
        return True
    elif "GEMINI_API_KEY" in os.environ and os.environ["GEMINI_API_KEY"]:
        return True
    return False


def vision():
    st.title("Vision: AI-Powered Content Generator")

    if not api_exists():
        show_instructions()
        return

    api_key = (st.secrets['api_key']["GEMINI_API_KEY"] or os.environ["GEMINI_API_KEY"])
    genai.configure(api_key=api_key)

    images = st.file_uploader(
        "Upload Image Files",
        type=["jpg", "png", "webp", "heic", "heif"],
        accept_multiple_files=True
    )

    prompt = st.text_input("Enter your prompt", placeholder="Type your prompt here...")
    if images and prompt and st.button("Generate"):
        oversized_files = [image.name for image in images if not validate_file_size(image)]
        if oversized_files:
            st.error(f"The following files exceed the 20MB size limit: {', '.join(oversized_files)}")
            return

        encoded_images = [
            {'mime_type': 'image/jpeg', 'data': base64.b64encode(image.read()).decode('utf-8')}
            for image in images
        ]

        try:
            model = genai.GenerativeModel(model_name="gemini-1.5-pro")
            response = model.generate_content(encoded_images + [prompt])
            st.subheader("Generated Response")
            st.text_area("Output", value=response.text, height=300)

        except Exception as e:
            st.error(f"An error occurred: {e}")
