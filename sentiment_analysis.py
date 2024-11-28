# sentiment_analysis.py
from transformers import pipeline

# Initialize sentiment analysis pipeline (use HuggingFace model or any other sentiment analysis model)
def analyze_sentiment(news_articles):
    sentiment_analyzer = pipeline("sentiment-analysis", model="yiyanghkust/finbert-tone")  # Use a model that works for financial sentiment
    sentiments = []
    
    for article in news_articles:
        sentiment = sentiment_analyzer(article['title'])[0]  # Analyzing the sentiment of the article title
        sentiments.append(sentiment['label'])
    
    # Return the most common sentiment from the articles
    if sentiments:
        return max(set(sentiments), key=sentiments.count)
    return "neutral"  # Default to neutral if no sentiment can be determined
