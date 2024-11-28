import yfinance as yf
import requests
from alpha_vantage.fundamentaldata import FundamentalData
import os

# Fetch stock data from Yahoo Finance
def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    stock_history = stock.history(period="1mo")  # Fetch historical data for 1 month
    stock_info = stock.info
    # Check if necessary data is available
    if 'currentPrice' not in stock_info:
        print(f"Warning: Missing 'currentPrice' for {ticker}.")
    
    return stock_history, stock_info

def fetch_stock_news(ticker):
    # Replace with your actual NewsAPI key
    api_key = 'API_KEY'  # Ensure your API key is set here
    url = f"https://newsapi.org/v2/everything?q={ticker}&apiKey={api_key}"
    response = requests.get(url)
    news_data = response.json()
    # Check if the 'articles' key exists
    if 'articles' in news_data:
        return news_data['articles']
    else:
        return []  


# Fetch financial data from Alpha Vantage
def fetch_financial_data(ticker):
    api_key = 'API_KEY'
    fd = FundamentalData(api_key)
    try:
        # Fetching the company overview
        company_overview, _ = fd.get_company_overview(ticker)
        return company_overview
    except Exception as e:
        print(f"Error fetching financial data: {e}")
        return None
