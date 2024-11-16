import joblib
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

# Load the trained model
def load_model():
    return joblib.load('models/stock_model.pkl')

# Load stock data from PostgreSQL
def load_stock_data():
    # Create connection string from environment variables
    conn_string = f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}'
    engine = create_engine(conn_string)

    # Read stock data from PostgreSQL
    data = pd.read_sql('SELECT * FROM stock_features', engine)
    return data

# Main function for loading model and making predictions
def main():
    # Load the model
    model = load_model()

    # Load stock data from PostgreSQL
    stock_data = load_stock_data()

    # Check the columns to see the exact name of the date column
    print("Columns in stock_data:", stock_data.columns)


    # Extract features for prediction
    features = stock_data[['50_MA', '200_MA', 'RSI', 'Volume']]

    # Make predictions
    predictions = model.predict(features)

    # Show predictions
    stock_data['Prediction'] = predictions
    print(stock_data[['Date', 'Prediction']])

if __name__ == "__main__":
    main()
