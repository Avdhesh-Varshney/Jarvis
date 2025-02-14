import librosa
import numpy as np
import tensorflow as tf
import soundfile as sf

# Load the pre-trained emotion detection model
MODEL_PATH = "emotion_model.h5"
model = tf.keras.models.load_model(MODEL_PATH)

# Emotion labels (Modify based on your model)
EMOTIONS = ["Neutral", "Happy", "Sad", "Angry", "Fearful", "Disgusted", "Surprised"]

def extract_features(audio_path):
    """Extract features from the audio file."""
    y, sr = librosa.load(audio_path, duration=3, offset=0.5)
    mfccs = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T, axis=0)
    return np.expand_dims(mfccs, axis=0)

def detect_emotion(audio_path):
    """Predict emotion from the given audio."""
    features = extract_features(audio_path)
    prediction = model.predict(features)
    emotion = EMOTIONS[np.argmax(prediction)]
    return emotion
