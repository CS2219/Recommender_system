# model_train.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import shap
import joblib

# Feature Engineering and Data Preparation
def prepare_data(df):
    """
    Prepare data by selecting the relevant features and handling missing values.
    """
    # Selecting relevant features from df_cleaned
    features = df[['MA_5', 'MA_10', 'RSI', 'Sentiment_Score', 'Close_Lag1', 'Close_Lag2', 'Price_Range']]
    target = df['Target']

    # Drop rows with missing values
    features = features.dropna()
    target = target.loc[features.index]

    return features, target

# Train Random Forest Classifier Model
def train_model(features, target):
    """
    Train a RandomForest model and save it.
    """
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    # Train the RandomForest model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Save the trained model
    joblib.dump(model, 'stock_predictor_model.pkl')
    
    return model

# SHAP explanation for model predictions
def explain_prediction(model, X_test, index):
    """
    Explain a prediction using SHAP values.
    """
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test.iloc[index:index+1])

    return shap_values

# Load the saved model
def load_model():
    """
    Load the saved model.
    """
    return joblib.load('stock_predictor_model.pkl')

# Train and save the model
def main():
    # Load your cleaned dataset
    df_cleaned = pd.read_csv('df_cleaned.csv')  # Adjust the path to your actual file

    # Prepare data
    features, target = prepare_data(df_cleaned)

    # Train model
    model = train_model(features, target)
    print("Model trained and saved!")

if __name__ == '__main__':
    main()
