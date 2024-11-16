import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    try:
        # Fetch the connection details from environment variables
        host = os.getenv('POSTGRES_HOST')
        port = os.getenv('POSTGRES_PORT')
        dbname = os.getenv('POSTGRES_DB')
        user = os.getenv('POSTGRES_USER')
        password = os.getenv('POSTGRES_PASSWORD')

        # Print connection details for debugging (without printing password)
        print(f"Attempting to connect to PostgreSQL at {host}:{port} with user '{user}'")

        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )

        print("Connection successful!")  # Debugging print

        return conn  # Returning the connection object

    except Exception as e:
        # If connection fails, print error message
        print(f"Error: Unable to connect to the database\n{e}")
        return None

# Calling the function to test
if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        conn.close()  # Close connection after testing
