import pickle
import os

# Path to the pre-trained model
MODEL_PATH = "path_to_your_trained_model.pkl"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Trained model file not found at {MODEL_PATH}")

# Load the trained model
with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)

def spamDetector(input_text):
    """
    Predicts whether the input_text is spam or not.

    Args:
        input_text (str): The text to classify.

    Returns:
        str: 'spam' or 'not spam'
    """
    # Preprocess the input (if necessary)
    processed_text = [input_text]
    
    # Predict using the loaded model
    prediction = model.predict(processed_text)
    return "spam" if prediction[0] == 1 else "not spam"
