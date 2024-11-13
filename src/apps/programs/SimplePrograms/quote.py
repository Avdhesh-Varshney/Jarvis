import streamlit as st
import requests

def quote():
    def get_quote():
        response = requests.get("https://zenquotes.io/api/today")
        if response.status_code == 200:
            return response.json()[0]
        else:
            return None

    st.title("Quote of the Day")

    quote = get_quote()
    box = st.empty()
    if quote:
        text = f"**{quote['q']}**\n\n— {quote['a']}"
        box.markdown(text)
    else:
        st.write("Couldn't fetch a quote at this moment. Please try again later.")