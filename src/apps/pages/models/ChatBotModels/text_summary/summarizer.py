from transformers import pipeline

# Initialize the summarization model (can be loaded once and reused)
def load_summarizer():
    summarizer = pipeline("summarization", model="t5-small")
    return summarizer

# Function to summarize the input text using the loaded model
def summarize_text(text):
    summarizer = load_summarizer()

    # Check if the text length is sufficient for summarization
    if len(text.split()) < 50:
        return "Please enter a text with at least 50 words."
    
    # Generate summary
    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
    return summary[0]['summary_text']
