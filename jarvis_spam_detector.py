import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pickle
import os

# Filepath for the saved model
MODEL_FILE = 'jarvis_spam_model.pkl'

# Function to train and save the model
def train_model():
    """
    Train the spam detection model using Naive Bayes and save it to a file.
    """
    print("Training model...")
    # Load dataset
    data = pd.read_csv('spam.csv', encoding='latin-1')
    data = data[['v1', 'v2']].rename(columns={'v1': 'label', 'v2': 'message'})
    data['label'] = data['label'].map({'ham': 0, 'spam': 1})

    # Create a pipeline for text preprocessing and classification
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english')),
        ('model', MultinomialNB())
    ])

    # Train the pipeline
    X = data['message']
    y = data['label']
    pipeline.fit(X, y)

    # Save the trained model to a file
    with open(MODEL_FILE, 'wb') as f:
        pickle.dump(pipeline, f)

    print("Model trained and saved successfully.")

# Function to predict if a message is spam or not
def predict_message(message: str) -> str:
    """
    Predict whether a given message is spam or not.

    Args:
        message (str): The input text message.

    Returns:
        str: "Spam" if the message is spam, otherwise "Not Spam".
    """
    # Check if the model file exists
    if not os.path.exists(MODEL_FILE):
        print("Model file not found. Training a new model...")
        train_model()

    # Load the trained model
    with open(MODEL_FILE, 'rb') as f:
        model = pickle.load(f)

    # Make a prediction
    prediction = model.predict([message])[0]
    return "Spam" if prediction == 1 else "Not Spam"

# Entry point for Jarvis integration
if __name__ == '__main__':
    # Train the model if it doesn't exist
    if not os.path.exists(MODEL_FILE):
        train_model()

    # Example interaction with Jarvis
    print("Welcome to the Spam Detection System!")
    while True:
        user_input = input("Enter a message to check (or type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        result = predict_message(user_input)
        print(f"Prediction: {result}")

