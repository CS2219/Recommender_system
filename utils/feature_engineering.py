# feature_engineering.py
import pandas as pd
import numpy as np

def feature_engineering(file_path='df_cleaned.csv'):
    """
    Load df_cleaned.csv, perform feature engineering, and return the updated DataFrame.
    """
    # Load the df_cleaned DataFrame from the CSV file
    df_cleaned = pd.read_csv(file_path)

    # Ensure Date column is a datetime object
    df_cleaned['Date'] = pd.to_datetime(df_cleaned['Date'])

    # Sort by Date for time-series calculations
    df_cleaned = df_cleaned.sort_values(by=['Ticker', 'Date'])

    # Calculate technical indicators
    df_cleaned['SMA_50'] = df_cleaned.groupby('Ticker')['Close'].transform(lambda x: x.rolling(window=50).mean())
    df_cleaned['EMA_50'] = df_cleaned.groupby('Ticker')['Close'].transform(lambda x: x.ewm(span=50, adjust=False).mean())

    # Bollinger Bands
    df_cleaned['Bollinger_Upper'] = df_cleaned['SMA_50'] + (df_cleaned['Close'].rolling(window=20).std() * 2)
    df_cleaned['Bollinger_Lower'] = df_cleaned['SMA_50'] - (df_cleaned['Close'].rolling(window=20).std() * 2)

    # Relative Strength Index (RSI)
    delta = df_cleaned['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df_cleaned['RSI'] = 100 - (100 / (1 + rs))

    # Lagged Features
    df_cleaned['Close_Lag1'] = df_cleaned.groupby('Ticker')['Close'].shift(1)
    df_cleaned['Close_Lag2'] = df_cleaned.groupby('Ticker')['Close'].shift(2)
    df_cleaned['Daily_Return'] = df_cleaned.groupby('Ticker')['Close'].pct_change()

    # Add sentiment-based features (assuming the Sentiment_Score column exists)
    df_cleaned['Positive_Sentiment'] = df_cleaned['Sentiment_Score'].apply(lambda x: 1 if x > 0 else 0)
    df_cleaned['Negative_Sentiment'] = df_cleaned['Sentiment_Score'].apply(lambda x: 1 if x < 0 else 0)

    # Drop rows with missing values after creating features
    df_cleaned = df_cleaned.dropna()

    return df_cleaned
