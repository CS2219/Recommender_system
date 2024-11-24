import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
from sqlalchemy import create_engine
from dotenv import load_dotenv
import streamlit as st
import os

# Load environment variables
load_dotenv()

# Load the trained model
model = joblib.load("models/stock_model.pkl")

# Function to load stock data
def load_stock_data(ticker):
    conn_string = f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}'
    engine = create_engine(conn_string)
    query = f'SELECT * FROM stock_prices WHERE "Ticker" = \'{ticker}\''
    data = pd.read_sql(query, engine)
    return data

# Main application
def main():
    st.title("Stock Recommendation System")
    st.write("Enter a stock ticker to get a Buy/Sell recommendation.")

    ticker = st.text_input("Enter Stock Ticker:", "")

    if st.button("Get Recommendation"):
        if not ticker:
            st.error("Please enter a stock ticker.")
            return

        # Load stock data
        data = load_stock_data(ticker)

        # Check if data is empty
        if data.empty:
            st.error("No data found for the given stock ticker.")
            return

        # Calculate features
        data['50_MA'] = data['Close'].rolling(window=50).mean()
        data['200_MA'] = data['Close'].rolling(window=200).mean()
        delta = data['Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        data['RSI'] = 100 - (100 / (1 + rs))

        # Prepare features for prediction
        features = data[['50_MA', '200_MA', 'RSI', 'Volume']].dropna()

        if features.empty:
            st.error("Insufficient data to calculate features for the given stock ticker.")
            return

        # Make prediction using the trained model
        predictions = model.predict(features)

        # Output the recommendation
        if predictions[-1] == 1:
            st.success("Recommendation: BUY")
        else:
            st.warning("Recommendation: SELL")

if __name__ == "__main__":
    main()
