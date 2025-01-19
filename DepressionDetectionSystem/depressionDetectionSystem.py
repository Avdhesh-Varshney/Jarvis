import streamlit as st
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torchaudio
import librosa
import numpy as np
from PIL import Image

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

def analyze_image(image_file):
    # You can add your image processing code here (e.g., face emotion detection)
    image = Image.open(image_file)
    # Example of displaying the image
    st.image(image, caption="Uploaded Image", use_column_width=True)
    # For simplicity, returning a mock analysis score
    return 0.7  # This can be changed with actual image processing logic

st.title("Depression Detection System")

# Load text model
model, tokenizer = load_text_model()

# Text input for depression detection
text_input = st.text_area("Enter your thoughts:")
if st.button("Analyze Text"):
    if text_input:
        depression_score = predict_text_depression(text_input, model, tokenizer)
        st.write(f"Depression Probability: {depression_score:.2f}")
    else:
        st.warning("Please enter text.")

# Audio input for depression detection
uploaded_audio = st.file_uploader("Upload an audio file (WAV, MP3)", type=["wav", "mp3"])
if uploaded_audio and st.button("Analyze Audio"):
    audio_score = analyze_audio(uploaded_audio)
    st.write(f"Depression Probability (from audio): {audio_score:.2f}")

# Image input for depression detection (PNG, JPEG, JPG)
uploaded_image = st.file_uploader("Upload an image (PNG, JPEG, JPG)", type=["png", "jpeg", "jpg"])
if uploaded_image and st.button("Analyze Image"):
    image_score = analyze_image(uploaded_image)
    st.write(f"Depression Probability (from image): {image_score:.2f}")

