# langchain_handler.py
import os
from transformers import pipeline
from google.cloud import language_v1
# Removed enums import, as it's no longer needed
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema import BaseOutputParser
from langchain.prompts import PromptTemplate
from langchain_community.tools import Tool


# Set up Google Cloud NLP client
client = language_v1.LanguageServiceClient()

# Hugging Face pipeline for text generation (reasoning and explanation)
reasoning_generator = pipeline("text-generation", model="gpt2")  # Example using GPT-2 for text generation

def analyze_sentiment_google_cloud(text: str) -> str:
    """
    Uses Google Cloud's NLP API to analyze sentiment of a text.
    """
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(document=document)
    
    sentiment_score = response.document_sentiment.score
    
    if sentiment_score > 0:
        return "positive"
    elif sentiment_score < 0:
        return "negative"
    else:
        return "neutral"


def generate_reasoning_explanation(prompt: str) -> str:
    """
    Uses Hugging Face's GPT-2 model for reasoning and explanation generation.
    """
    response = reasoning_generator(prompt, max_length=100)
    return response[0]["generated_text"]


class CustomOutputParser(BaseOutputParser):
    def parse(self, text: str) -> str:
        return text.strip()

# Define a template for stock recommendations
stock_recommendation_prompt = """
Based on the given stock news, generate a recommendation for the stock. 

Stock news: {news}

Recommendation:
"""

def get_stock_recommendation(news: str) -> str:
    """
    Generate a stock recommendation based on the given news using Hugging Face model for reasoning.
    """
    # Generate the prompt
    prompt = stock_recommendation_prompt.format(news=news)
    
    # Get reasoning and explanation using Hugging Face (GPT-2)
    reasoning = generate_reasoning_explanation(prompt)
    
    return reasoning


# Example usage for sentiment analysis and stock recommendation
def process_stock_news(news: str):
    sentiment = analyze_sentiment_google_cloud(news)
    print(f"Sentiment of the news: {sentiment}")
    
    recommendation = get_stock_recommendation(news)
    print(f"Stock Recommendation based on news: {recommendation}")

