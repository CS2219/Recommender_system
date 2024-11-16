import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load features from PostgreSQL
def load_features():
    # Create connection string from environment variables
    conn_string = f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}'
    engine = create_engine(conn_string)

    # Read feature data from PostgreSQL
    data = pd.read_sql('SELECT * FROM stock_features', engine)
    return data

# Train a model using the features
def train_model(data):
    X = data[['50_MA', '200_MA', 'RSI', 'Volume']]
    y = (data['Close'].shift(-1) > data['Close']).astype(int)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Save the trained model
    joblib.dump(model, 'models/stock_model.pkl')

# Main function to load features and train the model
def main():
    # Load features from PostgreSQL
    features = load_features()

    # Train the model
    train_model(features)

if __name__ == "__main__":
    main()
