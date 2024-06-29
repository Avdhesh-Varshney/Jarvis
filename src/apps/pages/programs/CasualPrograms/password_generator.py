import streamlit as st
import random
import string
import pyperclip

def password_generator_app():
    def generate_password(length, use_upper, use_lower, use_digits, use_special):
        characters = ''
        if use_upper:
            characters += string.ascii_uppercase
        if use_lower:
            characters += string.ascii_lowercase
        if use_digits:
            characters += string.digits
        if use_special:
            characters += string.punctuation

        if characters == '':
            st.error("Please select at least one character type!")
            return ""

        password = ''.join(random.choice(characters) for _ in range(length))
        return password

    # Streamlit app
    st.title("Password Generator")

    length = st.slider("Password length", min_value=4, max_value=30, value=8)
    use_upper = st.checkbox("Include A-Z", value=True)
    use_lower = st.checkbox("Include a-z", value=True)
    use_digits = st.checkbox("Include 0-9", value=True)
    use_special = st.checkbox("Include special characters", value=True)

    if "generated_password" not in st.session_state:
        st.session_state.generated_password = ""

    generate = st.button("Generate Password")
    if generate:
        st.session_state.generated_password = generate_password(length, use_upper, use_lower, use_digits, use_special)

    if st.session_state.generated_password:
        st.write("Generated Password:")
        st.code(st.session_state.generated_password, language="text")
        if st.button("Copy to Clipboard"):
            pyperclip.copy(st.session_state.generated_password)
            st.success("Password copied to clipboard!")
    else:
        st.write("No password generated yet. Please adjust the settings and click 'Generate Password'.")

password_generator_app()
