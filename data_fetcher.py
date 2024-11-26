import yfinance as yf
import requests
import pandas as pd

# Fetch stock data from Yahoo Finance
def get_stock_data_yahoo(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

# Fetch stock data from Alpha Vantage
def get_stock_data_alpha_vantage(ticker, api_key):
    url = f'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': ticker,
        'apikey': api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    if 'Time Series (Daily)' in data:
        df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
        df = df.rename(columns={'1. open': 'open', '2. high': 'high', '3. low': 'low', '4. close': 'close', '5. volume': 'volume'})
        df.index = pd.to_datetime(df.index)
        return df
    else:
        return pd.DataFrame()

# Fetch the latest news using NewsAPI
def get_latest_news(query, api_key):
    url = f'https://newsapi.org/v2/everything'
    params = {
        'q': query,
        'apiKey': api_key,
        'language': 'en',
        'pageSize': 5  # Get the latest 5 articles
    }
    response = requests.get(url, params=params)
    return response.json()['articles']
