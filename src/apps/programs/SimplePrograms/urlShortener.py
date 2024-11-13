import streamlit as st
import pyshorteners

def shorten_url(input_url):
    """Shortens the provided URL using TinyURL."""
    shortener = pyshorteners.Shortener()
    short_url = shortener.tinyurl.short(input_url)
    return short_url

# Main function for the Streamlit app
def urlShortener():
    st.title("🔗 URL Shortener")
    # Input the URL
    input_url = st.text_input("Enter URL to be shortened", "")
    # Submit button
    if st.button("✨ Shorten URL"):
        if input_url:  
            try:
                short_url = shorten_url(input_url)
                st.write(f"**Shortened URL:** {short_url}")  # Display the shortened URL
            except Exception as e:
                st.error(f"Error occurred: {e}")
        else:
            st.error("Please enter a valid URL.")

