import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load the pre-trained model
model = joblib.load('models/stock_model.pkl')

# Load your cleaned dataset once (it will be used for retrieving stock data)
df_cleaned = pd.read_csv('df_cleaned.csv')  # Update the path as needed

# Function to generate recommendation and explanation
def generate_recommendation(ticker):
    """
    Given the stock ticker, retrieve the stock's latest data and predict the recommendation.
    Also, provide a short textual explanation based on the prediction.
    """
    # Filter data for the given ticker
    stock_data = df_cleaned[df_cleaned['Ticker'] == ticker]

    if stock_data.empty:
        return "Error: Ticker not found in the dataset.", ""

    # Get the latest row of stock data (latest date)
    latest_data = stock_data.iloc[-1]

    # Prepare the input data for prediction
    input_features = pd.DataFrame({
        'SMA_50': [latest_data['SMA_50']],
        'EMA_50': [latest_data['EMA_50']],
        'RSI': [latest_data['RSI']],
        'Bollinger_Upper': [latest_data['Bollinger_Upper']],
        'Bollinger_Lower': [latest_data['Bollinger_Lower']]
    })

    # Predict using the trained model
    prediction = model.predict(input_features)
    
    # Prediction: 1 = Buy, 0 = Sell
    if prediction == 1:
        recommendation = "Buy"
        explanation = "Based on the technical indicators, the model predicts a potential upward trend, suggesting a buy opportunity."
    else:
        recommendation = "Sell"
        explanation = "The model predicts a potential downward trend, suggesting it may be a good time to sell."
    
    return recommendation, explanation

# Streamlit UI
def main():
    st.title("Stock Recommendation System")
    st.write("This app recommends whether you should buy or sell a stock based on recent market data.")

    # Input form for stock ticker
    st.subheader("Enter the stock ticker:")
    ticker = st.text_input("Stock Ticker (e.g., AAPL, MSFT, GOOG)")

    # When the user presses the 'Get Recommendation' button
    if st.button("Get Recommendation"):
        if not ticker:
            st.error("Please enter a stock ticker.")
        else:
            # Generate recommendation for the entered ticker
            recommendation, explanation = generate_recommendation(ticker.upper())

            # Display the result
            if recommendation == "Error: Ticker not found in the dataset.":
                st.error(recommendation)
            else:
                st.success(f"Recommendation: **{recommendation}**")
                st.write(f"**Explanation:** {explanation}")

if __name__ == "__main__":
    main()
