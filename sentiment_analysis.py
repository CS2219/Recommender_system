from transformers import pipeline

# Load Hugging Face sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

# Function to analyze sentiment of a news article
def analyze_sentiment(text):
    sentiment = sentiment_pipeline(text)
    return sentiment[0]['label']
