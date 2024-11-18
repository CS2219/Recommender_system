import pandas as pd
import psycopg2
from psycopg2 import sql

# PostgreSQL connection details
DB_PARAMS = {
    'dbname': '',  # Replace with your database name
    'user': 'postgres',
    'password': 'mypassword',
    'host': 'database-1.cj4qwuksc2n1.eu-north-1.rds.amazonaws.com',
    'port': '5432'
}

# Function to load the CSV data into PostgreSQL using INSERT statements
def load_csv_to_postgresql(csv_file_path, table_name="stock_alpha_news"):
    """Load data from a CSV file into PostgreSQL using explicit INSERT statements."""
    
    # Read the CSV file using pandas
    df = pd.read_csv(csv_file_path)
    
    # Ensure the columns are in the right order and format
    expected_columns = ['Ticker', 'Title', 'Published_Date', 'Source', 'Summary', 'URL']
    
    # Check if the CSV has the required columns
    if not all(col in df.columns for col in expected_columns):
        print("CSV file is missing required columns. Ensure the columns are: 'Ticker', 'Title', 'Published_Date', 'Source', 'Summary', 'URL'.")
        return
    
    # Ensure the 'Published_Date' column is in datetime format
    df['Published_Date'] = pd.to_datetime(df['Published_Date'], errors='coerce')
    
    # Connect to PostgreSQL
    try:
        connection = psycopg2.connect(
            dbname=DB_PARAMS['dbname'],
            user=DB_PARAMS['user'],
            password=DB_PARAMS['password'],
            host=DB_PARAMS['host'],
            port=DB_PARAMS['port']
        )
        cursor = connection.cursor()

        # Prepare the SQL insert statement template
        insert_query = sql.SQL("""
            INSERT INTO {} (ticker, title, published_date, source, summary, url)
            VALUES (%s, %s, %s, %s, %s, %s)
        """).format(sql.Identifier(table_name))
        
        # Iterate through the DataFrame and execute INSERT for each row
        for index, row in df.iterrows():
            values = (row['Ticker'], row['Title'], row['Published_Date'], row['Source'], row['Summary'], row['URL'])
            cursor.execute(insert_query, values)
        
        # Commit the transaction
        connection.commit()
        print(f"Data successfully inserted into {table_name} table.")
    
    except Exception as e:
        print(f"Error occurred while inserting data: {e}")
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Main function to load the CSV data
def main():
    # Path to the CSV file
    csv_file_path = '/workspaces/Recommender_system/all_tickers_news.csv'  # Replace with the path to your CSV file
    
    # Load data from the CSV file into PostgreSQL
    load_csv_to_postgresql(csv_file_path)

if __name__ == "__main__":
    main()
