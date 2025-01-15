import re
from sklearn.feature_extraction.text import TfidfVectorizer

class Preprocessor:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words="english", max_features=3000)

    def clean_text(self, text):
        text = re.sub(r"[^a-zA-Z\s]", "", text)  # Remove special characters
        text = re.sub(r"\s+", " ", text)         # Remove extra spaces
        return text.lower()

    def fit_transform(self, messages):
        cleaned_messages = [self.clean_text(msg) for msg in messages]
        return self.vectorizer.fit_transform(cleaned_messages)

    def transform(self, messages):
        cleaned_messages = [self.clean_text(msg) for msg in messages]
        return self.vectorizer.transform(cleaned_messages)
