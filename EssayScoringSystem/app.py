from flask import Flask, render_template, request
import numpy as np
from preprocess import preprocess_text
from model import load_model, predict_score

app = Flask(__name__)

# Load the trained model and vectorizer
model, vectorizer = load_model()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/score', methods=['POST'])
def score():
    if request.method == 'POST':
        essay = request.form['essay']
        # Preprocess the input essay
        essay_clean = preprocess_text(essay)
        # Predict the score
        predicted_score = predict_score(essay_clean, model, vectorizer)
        return render_template('result.html', score=predicted_score)

if __name__ == '__main__':
    app.run(debug=True)