from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from summarizer import summarize_text  # Import the summarization function

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Route for serving the HTML page
@app.route('/')
def index():
    return render_template('index.html')  # Serve the frontend HTML

# API route for summarizing the text
@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    text = data['text']

    # Use the summarize_text function from summarizer.py
    summary = summarize_text(text)

    # Return the summary as a JSON response
    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(debug=True)
