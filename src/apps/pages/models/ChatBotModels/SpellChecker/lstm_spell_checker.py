import streamlit as st
import numpy as np
import re
from src.apps.pages.models.ChatBotModels.SpellChecker.models.load_models import encoder_model, decoder_model, char2int, int2char, num_enc_tokens, num_dec_tokens

# Define functions for text processing and decoding
def process(sent):
    sent = sent.lower()
    sent = re.sub(r'[^0-9a-zA-Z ]', '', sent)
    sent = sent.replace('\n', '')
    return sent

def decode_sequence(input_seq):
    states_value = encoder_model.predict(input_seq)
    target_seq = np.zeros((1, 1, num_dec_tokens))
    target_seq[0, 0, char2int['\t']] = 1.

    decoded_sentence = ''
    stop_condition = False
    while not stop_condition:
        output_tokens, h, c = decoder_model.predict([target_seq] + states_value)
        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_char = int2char[sampled_token_index]
        decoded_sentence += sampled_char

        if (sampled_char == '\n' or len(decoded_sentence) > max_dec_len):
            stop_condition = True

        target_seq = np.zeros((1, 1, num_dec_tokens))
        target_seq[0, 0, sampled_token_index] = 1.

        states_value = [h, c]

    return decoded_sentence.strip()

def lstm_spelling_correction():
    st.title('LSTM Word Spelling Correction')

    input_text = st.text_input('Enter a sentence:', '')
    if input_text:
        input_text = process(input_text)
        input_seq = np.zeros((1, len(input_text), num_enc_tokens), dtype='float32')

        for t, char in enumerate(input_text):
            if char in char2int:
                input_seq[0, t, char2int[char]] = 1

        corrected_sentence = decode_sequence(input_seq.reshape((1, input_seq.shape[1], input_seq.shape[2])))
        st.text('Original Sentence: ' + input_text)
        st.text('Corrected Sentence: ' + corrected_sentence)
