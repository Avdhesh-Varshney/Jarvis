import streamlit as st
from PyMultiDictionary import MultiDictionary

def dictionary():
    st.write("Dictionary Lookup")
    word = st.text_input("Enter the Word:")
    if word:
        dictionary = MultiDictionary()
        choice = st.radio("Choose an Option", ['Meaning', 'Synonym', 'Antonym'])

        if choice == 'Meaning':
            meaning = dictionary.meaning('en', word)
            st.write(f"The meaning of '{word}' is: {meaning}")
        elif choice == 'Synonym':
            synonyms = dictionary.synonym('en', word)
            st.write(f"The synonyms of '{word}' are: {synonyms}")
        elif choice == 'Antonym':
            antonyms = dictionary.antonym('en', word)
            st.write(f"The antonyms of '{word}' are: {antonyms}")
    else:
        st.info("Enter a word to look up.", icon="📝")
