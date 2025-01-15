import numpy as np
import cv2
from keras.models import load_model
from keras.utils import np_utils

# Emotion dictionary
emotion_dict = {0: "Angry", 1: "Disgust", 2: "Fear", 3: "Happy", 4: "Sad", 5: "Surprise", 6: "Neutral"}

def preprocess_image(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    image = cv2.resize(image, (48, 48))  # Resize to match model input size
    image = image.astype('float32') / 255.0  # Normalize pixel values
    image = np.reshape(image, (1, 48, 48, 1))  # Add a channel dimension
    return image

def load_emotion_model():
    # Load the pre-trained model
    model = load_model('assets/emotion_model.h5')
    return model

def detect_emotion(frame, model):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        face = preprocess_image(face)  # Preprocess the face for emotion prediction
        emotion_pred = model.predict(face)  # Get prediction
        max_index = np.argmax(emotion_pred[0])  # Get the emotion with highest probability
        emotion = emotion_dict[max_index]  # Get emotion name
        color = (0, 255, 0)  # Color for bounding box (green)
        
        # Draw the rectangle and emotion label on the frame
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    
    return frame

def run_emotion_detection():
    model = load_emotion_model()
    cap = cv2.VideoCapture(0)  # Start webcam

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = detect_emotion(frame, model)
        cv2.imshow('Emotion Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit if 'q' is pressed
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    run_emotion_detection()  # Run the emotion detection function when this script is executed
