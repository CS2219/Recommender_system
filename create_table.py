import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Establish a connection to the PostgreSQL database
try:
    conn = psycopg2.connect(
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT'),
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD')
    )
    conn.autocommit = True
    print("Connected to the database successfully.")
except Exception as e:
    print(f"Connection error: {e}")

# Create a cursor
cursor = conn.cursor()

# Define the SQL query to create the table
create_table_query = """
CREATE TABLE IF NOT EXISTS stock_prices (
    id SERIAL PRIMARY KEY,
    Date DATE NOT NULL,
    Ticker VARCHAR(10) NOT NULL,
    Open NUMERIC,
    High NUMERIC,
    Low NUMERIC,
    Close NUMERIC,
    Adj_Close NUMERIC,
    Volume BIGINT
);
"""

# Execute the query
try:
    cursor.execute(create_table_query)
    print("Table 'stock_prices' created successfully.")
except Exception as e:
    print(f"Error creating table: {e}")

# Close the cursor and connection
cursor.close()
conn.close()
