import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
import lime
import lime.lime_tabular
import joblib

# Feature Engineering Function
def feature_engineering(file_path='df_cleaned.csv'):
    """
    Load df_cleaned_updated.csv, perform feature engineering, and return the updated DataFrame.
    """
    # Load the df_cleaned DataFrame from the CSV file
    df_cleaned = pd.read_csv(file_path)

    # Ensure Date column is a datetime object
    df_cleaned['Date'] = pd.to_datetime(df_cleaned['Date'])

    # Sort by Date for time-series calculations
    df_cleaned = df_cleaned.sort_values(by=['Ticker', 'Date'])

    # Calculate technical indicators
    df_cleaned['SMA_50'] = df_cleaned.groupby('Ticker')['Close'].transform(lambda x: x.rolling(window=50).mean())
    df_cleaned['EMA_50'] = df_cleaned.groupby('Ticker')['Close'].transform(lambda x: x.ewm(span=50, adjust=False).mean())

    # Bollinger Bands
    df_cleaned['Bollinger_Upper'] = df_cleaned['SMA_50'] + (df_cleaned['Close'].rolling(window=20).std() * 2)
    df_cleaned['Bollinger_Lower'] = df_cleaned['SMA_50'] - (df_cleaned['Close'].rolling(window=20).std() * 2)

    # Relative Strength Index (RSI)
    delta = df_cleaned['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df_cleaned['RSI'] = 100 - (100 / (1 + rs))

    # Lagged Features
    df_cleaned['Close_Lag1'] = df_cleaned.groupby('Ticker')['Close'].shift(1)
    df_cleaned['Close_Lag2'] = df_cleaned.groupby('Ticker')['Close'].shift(2)
    df_cleaned['Daily_Return'] = df_cleaned.groupby('Ticker')['Close'].pct_change()

    # Add sentiment-based features (assuming the Sentiment_Score column exists)
    df_cleaned['Positive_Sentiment'] = df_cleaned['Sentiment_Score'].apply(lambda x: 1 if x > 0 else 0)
    df_cleaned['Negative_Sentiment'] = df_cleaned['Sentiment_Score'].apply(lambda x: 1 if x < 0 else 0)

    # Drop rows with missing values after creating features
    df_cleaned = df_cleaned.dropna()

    return df_cleaned

# Load and perform feature engineering
df_cleaned = feature_engineering('df_cleaned.csv')

# Define features (X) and target (y)
X = df_cleaned[['SMA_50', 'EMA_50', 'Bollinger_Upper', 'Bollinger_Lower', 'RSI', 'Sentiment_Score', 
                'Close_Lag1', 'Close_Lag2', 'Daily_Return', 'Positive_Sentiment', 'Negative_Sentiment']]
y = df_cleaned['Target']  # Target variable: 1=BUY, 0=SELL

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Apply StandardScaler to the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # Scale test data using the same scaler

# Train RandomForest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')  # Use class_weight if the classes are imbalanced
model.fit(X_train_scaled, y_train)

# Evaluate the model
y_pred = model.predict(X_test_scaled)
print("Model Evaluation Report:")
print(classification_report(y_test, y_pred))

# Save the model
joblib.dump(model, 'stock_recommender_model.pkl')
print("Model saved as 'stock_recommender_model.pkl'.")

# LIME Explanation
explainer_lime = lime.lime_tabular.LimeTabularExplainer(
    X_train_scaled, 
    training_labels=y_train.values, 
    mode='classification', 
    feature_names=X.columns,
    class_names=['SELL', 'BUY'],  # Assuming binary classification, where 0=SELL, 1=BUY
    discretize_continuous=True  # Discretize continuous variables for LIME
)

# Choose an instance for explanation (e.g., first instance of the test set)
i = 0  # You can change this to any test instance you want to explain

# Generate explanation
exp = explainer_lime.explain_instance(X_test_scaled[i], model.predict_proba, num_features=5)

# Display the explanation (This will show the LIME explanation in a notebook or output)
exp.show_in_notebook()
