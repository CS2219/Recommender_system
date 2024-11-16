import yfinance as yf
import pandas as pd
import psycopg2
from sqlalchemy import create_engine, types
import logging
import os

# Enable logging to capture the SQL queries being executed
logging.basicConfig(level=logging.DEBUG)

# Fetch stock data from Yahoo Finance (for example, Apple stock)
def fetch_yahoo_finance_data(ticker: str):
    stock = yf.Ticker(ticker)
    stock_data = stock.history(period="1mo")  # Collect the last month of data
    
    # Check if data is empty and print for debugging
    if stock_data.empty:
        print(f"No data fetched for {ticker}")
    else:
        print(f"Data fetched for {ticker}:")
        print(stock_data.head())  # Print the first few rows of the data
    
    stock_data['Ticker'] = ticker  # Add the ticker to the data to identify it
    return stock_data

# Store data in PostgreSQL
def store_in_postgres(data, table_name="stock_prices"):
    # Database connection details
    host = "database-1.cj4qwuksc2n1.eu-north-1.rds.amazonaws.com"
    dbname = ""  # Replace with your database name
    user = "postgres"
    password = "mypassword"

    # Ensure data types are compatible with PostgreSQL
    dtype = {
        'Open': types.Float(),
        'High': types.Float(),
        'Low': types.Float(),
        'Close': types.Float(),
        'Volume': types.Integer(),
        'Dividends': types.Float(),
        'Stock Splits': types.Float(),
        'Date': types.DateTime(),  # Date is datetime in Yahoo Finance
        'Ticker': types.String(10)  # Ticker column
    }

    # Create an engine for the connection
    engine = create_engine(f'postgresql://{user}:{password}@{host}/{dbname}')
    
    # Check for missing data and clean it (optional step)
    data = data.fillna("")  # Replace NaNs with empty strings or handle as appropriate
    
    # Debug: Print data before insertion
    print(f"Preparing to insert data for {data['Ticker'][0]}")
    print(data.head())  # Print the first few rows of data to ensure it's correct

    try:
        with engine.connect() as conn:
            # Insert data into PostgreSQL, replacing any existing data in the table
            data.to_sql(table_name, conn, if_exists='append', index=True, dtype=dtype)
            print(f"Data successfully stored for {data['Ticker'][0]} in {table_name} table.")
    except Exception as e:
        print(f"Error occurred while inserting data for {data['Ticker'][0]}: {e}")
        logging.error(f"Error occurred while inserting data for {data['Ticker'][0]}: {e}")

# Main function to fetch data for multiple tickers and store in PostgreSQL
def main():
    # Step 1: Manually define the list of tickers for the technology sector
    tickers = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "FB", "NVDA", "TSLA", "INTC", "CSCO", "ORCL",
        "IBM", "SAP", "CRM", "AMD", "PYPL", "SOFI", "ADBE", "QCOM", "VZ", "TWTR"
    ]

    # Step 2: Fetch stock data for each ticker and store it in PostgreSQL
    for ticker in tickers:
        print(f"Fetching data for {ticker}...")
        data = fetch_yahoo_finance_data(ticker)  # Fetch data for the ticker
        if data.empty:
            print(f"No data fetched for {ticker}. Skipping insertion.")
        else:
            store_in_postgres(data, "stock_prices")  # Store data in PostgreSQL

if __name__ == "__main__":
    main()


