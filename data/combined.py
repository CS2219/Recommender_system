import pandas as pd
from sqlalchemy import create_engine

# Database connection parameters (example for PostgreSQL)
db_username = 'postgres'
db_password = 'mypassword'
db_host = 'database-1.cj4qwuksc2n1.eu-north-1.rds.amazonaws.com'
db_port = '5432'
db_name = 'postgres'

# Create a connection string
connection_string = f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'

# Create a database engine
engine = create_engine(connection_string)

# SQL queries to fetch data from each table
queries = {
    "stock_price": "SELECT * FROM stock_prices",
    "news_article": "SELECT * FROM news_article",
    "stock_alpha_news": "SELECT * FROM stock_alpha_news"
}

# Fetch data into pandas DataFrames
try:
    # Fetch stock_price_df
    stock_price_df = pd.read_sql(queries["stock_price"], engine)
    print("Stock Price DataFrame created successfully!")
    print("Stock Price DataFrame - Head and Data Types:")
    print(stock_price_df.head())  # Show first 5 rows
    print(stock_price_df.dtypes)  # Show column data types

    # Fetch news_article_df
    news_article_df = pd.read_sql(queries["news_article"], engine)
    print("News Article DataFrame created successfully!")
    print("News Article DataFrame - Head and Data Types:")
    print(news_article_df.head())  # Show first 5 rows
    print(news_article_df.dtypes)  # Show column data types

    # Fetch stock_alpha_news_df
    stock_alpha_news_df = pd.read_sql(queries["stock_alpha_news"], engine)
    print("Stock Alpha News DataFrame created successfully!")
    print("Stock Alpha News DataFrame - Head and Data Types:")
    print(stock_alpha_news_df.head())  # Show first 5 rows
    print(stock_alpha_news_df.dtypes)  # Show column data types

except Exception as e:
    print(f"Error occurred while fetching data: {e}")

# If DataFrames are successfully created, proceed with the conversion and merging
try:
    # Convert 'published_date' to datetime, then extract only the date part
    stock_price_df['published_date'] = pd.to_datetime(stock_price_df['published_date'], errors='coerce').dt.date
    news_article_df['published_date'] = pd.to_datetime(news_article_df['published_date'], errors='coerce').dt.date
    stock_alpha_news_df['published_date'] = pd.to_datetime(stock_alpha_news_df['published_date'], errors='coerce').dt.date

    # After conversion, check the data types of 'published_date'
    print("\nAfter Conversion - Data Types:")
    print(stock_price_df.dtypes)
    print(news_article_df.dtypes)
    print(stock_alpha_news_df.dtypes)

    # Merge the dataframes on 'Ticker' and 'published_date'
    merged_df = stock_price_df.merge(news_article_df, on=['Ticker', 'published_date'], how='outer')
    merged_df = merged_df.merge(stock_alpha_news_df, on=['Ticker', 'published_date'], how='outer')

    # Debugging: Print the first few rows of the merged DataFrame and its data types
    print("\nMerged DataFrame - Head and Data Types:")
    print(merged_df.head())  # Show first 5 rows of merged data
    print(merged_df.dtypes)  # Show column data types of merged DataFrame

    # Export the merged dataframe to a single CSV file
    merged_df.to_csv('merged_stock_data.csv', index=False)

    print("Merged data exported to CSV successfully!")

except Exception as e:
    print(f"Error occurred during data processing: {e}")
