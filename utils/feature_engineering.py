import pandas as pd
import numpy as np
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Calculate moving averages and RSI
def calculate_features(data):

    # Calculate 50-day and 200-day moving averages
    data['50_MA'] = data['Close'].rolling(window=50).mean()
    data['200_MA'] = data['Close'].rolling(window=200).mean()

    # Calculate Relative Strength Index (RSI)
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + rs))

    # Calculate Volume-based Feature (for simplicity, let's use Volume itself)
    data['Volume'] = data['Volume']

    return data

# Load stock data from PostgreSQL
def load_stock_data():
    # Create connection string from environment variables
    conn_string = f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}'
    engine = create_engine(conn_string)

    # Read stock data from PostgreSQL
    data = pd.read_sql('SELECT * FROM stock_prices', engine)
    return data

# Save features back to PostgreSQL
def save_features_to_postgres(features):
    # Create connection string from environment variables
    conn_string = f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}'
    engine = create_engine(conn_string)

    # Save the calculated features back to the database
    features.to_sql('stock_features', engine, if_exists='replace', index=False)

# Main function for feature engineering
def main():
    # Load stock data from PostgreSQL
    stock_data = load_stock_data()

    # Perform feature engineering
    features = calculate_features(stock_data)

    # Save the calculated features back to the database
    save_features_to_postgres(features)

if __name__ == "__main__":
    main()
