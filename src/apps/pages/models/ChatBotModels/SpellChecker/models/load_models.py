import numpy as np
from keras.models import load_model

# Load LSTM models and character dictionaries
encoder_model = load_model('encoder.h5')
decoder_model = load_model('decoder.h5')

char_set = list(" abcdefghijklmnopqrstuvwxyz0123456789")
char2int = {char_set[x]: x for x in range(len(char_set))}
int2char = {char2int[x]: x for x in char_set}
count = len(char_set)
codes = ["\t", "\n", '#']
for i in range(len(codes)):
    code = codes[i]
    char2int[code] = count
    int2char[count] = code
    count += 1

num_enc_tokens = len(char_set)
num_dec_tokens = len(char_set) + 2  # includes \n \t
