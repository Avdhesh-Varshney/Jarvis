import os
import cv2
import dlib
import numpy as np
from flask import Flask, render_template, request, redirect, url_for
from fer import FER

app = Flask(__name__)

UPLOAD_FOLDER = 'data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Initialize Dlib's face detector
detector = dlib.get_frontal_face_detector()
# Initialize the FER emotion detector
emotion_detector = FER()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if 'image_file' not in request.files:
        return "No file part in the request"
    
    file = request.files['image_file']
    if file.filename == '':
        return "No file selected"
    
    if file:
        # Save the uploaded file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Read the image and convert to grayscale for face detection
        image = cv2.imread(filepath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = detector(gray)

        if len(faces) == 0:
            return "No faces detected in the image"

        # Process each face in the image
        emotions = []
        for face in faces:
            # Extract the region of interest (ROI) where the face is
            x, y, w, h = (face.left(), face.top(), face.width(), face.height())
            roi = image[y:y+h, x:x+w]

            # Detect emotions for the detected face using FER
            emotion, score = emotion_detector.top_emotion(roi)
            emotions.append((emotion, score))

        # Analyze emotions
        if emotions:
            # Sort by the highest emotion score
            most_common_emotion = max(emotions, key=lambda x: x[1])
            emotion, score = most_common_emotion
            message = f"The most prominent emotion detected is {emotion} with a confidence score of {score:.2f}."
        else:
            message = "No emotion detected"

        return render_template('result.html', message=message)

    return "File upload failed"

if __name__ == '__main__':
    app.run(debug=True)
