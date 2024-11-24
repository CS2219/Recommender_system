import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load environment variables
load_dotenv()

# Function to load features from PostgreSQL
def load_features():
    conn_string = f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}'
    engine = create_engine(conn_string)

    # Read the features table
    data = pd.read_sql('SELECT * FROM stock_features', engine)
    return data

# Function to train the model
def train_model(data):
    # Define the feature set and the target variable
    X = data[['50_MA', '200_MA', 'RSI', 'Volume']]
    y = (data['Close'].shift(-1) > data['Close']).astype(int).fillna(0)  # Binary target: 1 (Buy), 0 (Sell)

    # Split the dataset into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a RandomForestClassifier
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.2f}")

    # Save the trained model
    model_path = 'models/stock_model2.pkl'
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

# Main function
def main():
    # Load the features
    features = load_features()

    # Train the model
    train_model(features)

if __name__ == "__main__":
    main()
