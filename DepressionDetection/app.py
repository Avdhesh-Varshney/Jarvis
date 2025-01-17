import streamlit as st
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torchaudio
import librosa
import numpy as np

def load_text_model():
    model_name = "distilbert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)  # 0: Not Depressed, 1: Depressed
    return model, tokenizer

def predict_text_depression(text, model, tokenizer):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    return probs[0][1].item()  # Probability of being depressed

def analyze_audio(audio_file):
    y, sr = librosa.load(audio_file, sr=16000)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mean_mfccs = np.mean(mfccs, axis=1)
    score = np.mean(mean_mfccs) / 100  # Basic normalization
    return min(max(score, 0), 1)  # Ensure within [0,1]

st.title("Depression Detection NLP Model")

model, tokenizer = load_text_model()

text_input = st.text_area("Enter your thoughts:")
if st.button("Analyze Text"):
    if text_input:
        depression_score = predict_text_depression(text_input, model, tokenizer)
        st.write(f"Depression Probability: {depression_score:.2f}")
    else:
        st.warning("Please enter text.")

uploaded_audio = st.file_uploader("Upload an audio file (WAV/MP3)", type=["wav", "mp3"])
if uploaded_audio and st.button("Analyze Audio"):
    audio_score = analyze_audio(uploaded_audio)
    st.write(f"Depression Probability (from audio): {audio_score:.2f}")