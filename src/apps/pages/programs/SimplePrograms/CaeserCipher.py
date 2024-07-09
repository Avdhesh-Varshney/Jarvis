import streamlit as st

def caeserCipher():
    st.title("Caeser Cipher")
    word = st.text_input("Enter the word")
    level = st.slider("enter the key",1,100)
    operation = st.selectbox("Operation: ", ['Encode', 'Decode'])

    def cipher(start_text, shift_amount, cipher_direction):
        end_text = ""
        if cipher_direction == 'Encode':
            for c in start_text:
                if c.isalpha():
                    ascii_code = ord(c)
                    if c.isupper():
                        ascii_code = (ascii_code - ord('A') + shift_amount) % 26 + ord('A')
                    else:
                        ascii_code = (ascii_code - ord('a') + shift_amount) % 26 + ord('a')
                    end_text += chr(ascii_code)
                else:
                    end_text += c

        if cipher_direction == "Decode":
            for c in start_text:
                if c.isalpha():
                    ascii_code = ord(c)
                    if c.isupper():
                        ascii_code = (ascii_code - ord('A') - shift_amount) % 26 + ord('A')
                    else:
                        ascii_code = (ascii_code - ord('a') - shift_amount) % 26 + ord('a')
                    end_text += chr(ascii_code)
                else:
                    end_text += c
        st.success(end_text)
    if(st.button('Generate')):
        if word == "":
            st.warning("You have not given any input")
        else:
            cipher(start_text=word,shift_amount=level,cipher_direction=operation)
