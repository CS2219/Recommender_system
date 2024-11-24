import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, roc_auc_score, roc_curve
import seaborn as sns
import matplotlib.pyplot as plt

# Feature Engineering
def feature_engineering(data):
    """
    Perform feature engineering on the stock data.
    This function calculates common technical indicators like SMA, EMA, Bollinger Bands, and RSI.
    """
    # Ensure Date column is a datetime object
    data['Date'] = pd.to_datetime(data['Date'])

    # Sort by Date for time-series calculations
    data = data.sort_values(by='Date')

    # Calculate Simple Moving Average (SMA) over a 50-day window
    data['SMA_50'] = data['Close'].rolling(window=50).mean()

    # Calculate Exponential Moving Average (EMA) over a 50-day window
    data['EMA_50'] = data['Close'].ewm(span=50, adjust=False).mean()

    # Calculate Bollinger Bands (upper and lower)
    data['Bollinger_Upper'] = data['SMA_50'] + (data['Close'].rolling(window=20).std() * 2)
    data['Bollinger_Lower'] = data['SMA_50'] - (data['Close'].rolling(window=20).std() * 2)

    # Calculate Relative Strength Index (RSI)
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + rs))

    # Drop rows with missing values (important for models)
    data = data.dropna()

    return data

# Model Training and Evaluation
def train_model(data):
    """
    Train a RandomForest model using the stock data after performing feature engineering.
    Save the trained model to disk and evaluate performance.
    """
    # Perform feature engineering
    data = feature_engineering(data)

    # Define the features (X) and target variable (y)
    features = ['SMA_50', 'EMA_50', 'RSI', 'Bollinger_Upper', 'Bollinger_Lower']
    
    # Ensure the 'Target' column exists; it should indicate Buy (1) or Sell (0)
    if 'Target' not in data.columns:
        raise ValueError("The 'Target' column is missing from the dataset.")

    # Features (X) and Target (y)
    X = data[features]
    y = data['Target']

    # Split the data into training and testing sets (80% training, 20% testing)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the Random Forest Classifier model with class weights to handle imbalance
    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')

    # Train the model on the training set
    model.fit(X_train, y_train)

    # Predict on the test set
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]  # Get probabilities for the positive class (Buy)

    # Evaluate the model's performance
    print("Model Performance on Test Data:")
    print(classification_report(y_test, y_pred))

    # Accuracy Score
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print("Confusion Matrix:")
    print(cm)

    # Plot Confusion Matrix
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=['Sell', 'Buy'], yticklabels=['Sell', 'Buy'])
    plt.title('Confusion Matrix')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.show()

    # AUC-ROC
    auc_roc = roc_auc_score(y_test, y_prob)
    print(f"AUC-ROC: {auc_roc:.2f}")

    # Plot AUC-ROC Curve
    fpr, tpr, thresholds = roc_curve(y_test, y_prob)
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='blue', label=f'AUC = {auc_roc:.2f}')
    plt.plot([0, 1], [0, 1], color='gray', linestyle='--')
    plt.title('ROC Curve')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend(loc='lower right')
    plt.show()

    # Save the trained model to a file
    joblib.dump(model, 'models/stock_model.pkl')
    print("Model saved as 'models/stock_model.pkl'")

# Main function to execute the workflow
def main():
    """
    Main function to load data, train the model, evaluate performance, and save it.
    """
    # Load the cleaned dataset (df_cleaned)
    df_cleaned = pd.read_csv('df_cleaned.csv')  # Adjust this path to your actual file location

    # Train the model using df_cleaned
    train_model(df_cleaned)

if __name__ == "__main__":
    main()
