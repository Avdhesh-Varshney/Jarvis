import pickle
from utils.preprocess import Preprocessor

# Load model and vectorizer
with open("utils/model.pkl", "rb") as model_file, open("utils/vectorizer.pkl", "rb") as vec_file:
    model = pickle.load(model_file)
    vectorizer = pickle.load(vec_file)

def predict_message(message):
    preprocessor = Preprocessor()
    transformed_message = vectorizer.transform([preprocessor.clean_text(message)])
    prediction = model.predict(transformed_message)[0]
    confidence = model.predict_proba(transformed_message).max()
    return ("Spam" if prediction == 1 else "Not Spam", confidence)
