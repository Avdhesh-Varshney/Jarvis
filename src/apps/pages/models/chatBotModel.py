import streamlit as st
from src.apps.pages.models.ChatBotModels.SpellChecker.lstm_spell_checker import lstm_spelling_correction

def main():
    st.title('ChatBot Models')
    choice = st.selectbox('Choose any model', ['LSTM Spelling Correction'])

    st.markdown('---')

    if choice == 'LSTM Spelling Correction':
        lstm_spelling_correction()

if __name__ == "__main__":
    main()
