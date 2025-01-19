from flask import Flask, request, render_template
import os
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import cv2
import numpy as np

app = Flask(__name__)

# Ensure 'uploads' directory exists
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Load NLP Depression Detection Model
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)  # 0: Not Depressed, 1: Depressed

# Function to analyze text for depression
def predict_text_depression(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    return probs[0][1].item()  # Probability of being depressed

# Function to analyze face emotions using OpenCV
def analyze_face(image_path):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    image = cv2.imread(image_path)

    if image is None:
        return "Error: Cannot load image."

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    if len(faces) == 0:
        return "No face detected."

    # Placeholder emotion detection (to be replaced with a deep learning model)
    return "Face detected: Possible neutral or happy expression."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    text_depression_score = None
    face_analysis_result = None

    # Handle chat file upload
    chat_file = request.files.get("chat_file")
    if chat_file:
        chat_path = os.path.join(app.config["UPLOAD_FOLDER"], "chat.txt")
        chat_file.save(chat_path)
        
        with open(chat_path, "r", encoding="utf-8") as f:
            chat_text = f.read()
        
        text_depression_score = predict_text_depression(chat_text)

    # Handle image file upload
    image_file = request.files.get("image_file")
    if image_file:
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], "image.jpg")
        image_file.save(image_path)
        face_analysis_result = analyze_face(image_path)
    
    return render_template("result.html", text_score=text_depression_score, face_result=face_analysis_result)

if __name__ == "__main__":
    app.run(debug=True)
