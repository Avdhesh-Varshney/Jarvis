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

    # app
    st.title("Password Generator")


    length = st.slider("Password length", min_value=6, max_value=24, value=12)
    use_upper = st.checkbox("Include A-Z", value=True)
    use_lower = st.checkbox("Include a-z", value=True)
    use_digits = st.checkbox("Include 0-9", value=True)
    use_special = st.checkbox("Include special characters", value=True)

    # store settings in session state
    if 'password' not in st.session_state:  
        st.session_state.password = ""
        st.session_state.last_settings = {
            "length": length,
            "use_upper": use_upper,
            "use_lower": use_lower,
            "use_digits": use_digits,
            "use_special": use_special
        }

    def settings_changed(): 
        return (length != st.session_state.last_settings["length"] or
                use_upper != st.session_state.last_settings["use_upper"] or
                use_lower != st.session_state.last_settings["use_lower"] or
                use_digits != st.session_state.last_settings["use_digits"] or
                use_special != st.session_state.last_settings["use_special"])

    if st.button("Generate Password"):  
        st.session_state.password = generate_password(length, use_upper, use_lower, use_digits, use_special)
        st.session_state.last_settings = {
            "length": length,
            "use_upper": use_upper,
            "use_lower": use_lower,
            "use_digits": use_digits,
            "use_special": use_special
        }

    if st.session_state.password:
        st.write("Generated Password:")
        st.code(st.session_state.password, language="text")
        if st.button("Copy to Clipboard"):
            pyperclip.copy(st.session_state.password)
            st.success("Password copied to clipboard!")
    else:
        st.write("No password generated yet. Please adjust the settings and click 'Generate Password'.")

password_generator_app()