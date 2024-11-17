import pandas as pd
from sqlalchemy import create_engine, types
import psycopg2

# PostgreSQL connection details
DB_PARAMS = {
    'dbname': '',  # Replace with your database name
    'user': 'postgres',
    'password': 'mypassword',
    'host': 'database-1.cj4qwuksc2n1.eu-north-1.rds.amazonaws.com',
    'port': '5432'
}

# Function to load the CSV data into PostgreSQL
def load_csv_to_postgresql(csv_file_path, table_name="stock_alpha_news"):
    """Load data from a CSV file into PostgreSQL."""
    # Read the CSV file using pandas
    df = pd.read_csv(csv_file_path)

    # Ensure the columns are in the right order and format
    # This assumes the CSV columns match the following structure:
    expected_columns = ['Ticker', 'Title', 'Published_Date', 'Source', 'Summary', 'URL']

    # Check if the CSV has the required columns
    if not all(col in df.columns for col in expected_columns):
        print("CSV file is missing required columns. Ensure the columns are: 'ticker', 'title', 'published_date', 'source', 'summary', 'url'.")
        return

    # Ensure the 'published_date' column is in datetime format
    df['Published_Date'] = pd.to_datetime(df['Published_Date'], errors='coerce')

    # Ensure data types are compatible with PostgreSQL
    dtype = {
        'ticker': types.String(10),
        'title': types.Text(),
        'published_date': types.DateTime(),
        'source': types.String(255),
        'summary': types.Text(),
        'url': types.Text()
    }

    # Create SQLAlchemy engine for PostgreSQL connection
    engine = create_engine(f'postgresql://{DB_PARAMS["user"]}:{DB_PARAMS["password"]}@{DB_PARAMS["host"]}/{DB_PARAMS["dbname"]}')
    
    # Insert data into PostgreSQL, appending if the table already exists
    try:
        with engine.connect() as conn:
            # Insert data into PostgreSQL, replacing any existing data in the table
            df.to_sql(table_name, conn, if_exists='append', index=False, dtype=dtype)
            print(f"Data successfully loaded into {table_name} table.")
    except Exception as e:
        print(f"Error occurred while inserting data: {e}")
    finally:
        conn.close()

# Main function to load the CSV data
def main():
    # Path to the CSV file
    csv_file_path = '/workspaces/Recommender_system/all_tickers_news.csv'  # Replace with the path to your CSV file
    
    # Load data from the CSV file into PostgreSQL
    load_csv_to_postgresql(csv_file_path)

if __name__ == "__main__":
    main()
