import openai
import shap
import joblib
import pandas as pd
import numpy as np
import streamlit as st

# Load OpenAI API Key for Generative AI
openai.api_key = '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'

# Load model and scaler
model = joblib.load('stock_recommender_model.pkl')
#scaler = joblib.load('scaler.pkl')

# Function to Generate Explanations Using GPT-3
def generate_explanation(shap_values, feature_names):
    prompt = "Explain the following SHAP values for stock recommendation in human-friendly language:\n"
    for i, feature in enumerate(feature_names):
        prompt += f"Feature: {feature}, SHAP Value: {shap_values[i]:.4f}\n"
    
    # Request explanation from GPT-3
    response = openai.Completion.create(
        engine="text-davinci-003",  # or "gpt-4" if available
        prompt=prompt,
        max_tokens=150
    )
    
    explanation = response.choices[0].text.strip()
    return explanation

# Streamlit UI Setup
st.title("Stock Recommendation System")
ticker = st.text_input("Enter stock ticker (e.g., AAPL, MSFT):")

# Load the cleaned dataset
df_cleaned = pd.read_csv('df_cleaned.csv')

# Function to get recommendation and explanation
def get_recommendation(ticker):
    stock_data = df_cleaned[df_cleaned['Ticker'] == ticker].tail(1)
    
    if stock_data.empty:
        st.write(f"Sorry, no data available for ticker {ticker}.")
        return

    input_features = stock_data[['SMA_50', 'EMA_50', 'Bollinger_Upper', 'Bollinger_Lower', 'RSI', 'Sentiment_Score', 'Close_Lag1', 'Daily_Return']]
    input_scaled = scaler.transform(input_features)

    # Make prediction
    prediction = model.predict(input_scaled)

    if prediction == 1:
        st.write(f"Recommendation for {ticker}: **BUY**")
    else:
        st.write(f"Recommendation for {ticker}: **SELL**")
    
    # Explain the prediction using SHAP values
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(input_scaled)

    if isinstance(shap_values, list):
        shap_values = shap_values[1]  # For binary classification, use the positive class

    # Generate explanation for the top features using Generative AI (GPT-3)
    explanation = generate_explanation(shap_values[0], input_features.columns)
    
    st.subheader("Model Explanation")
    st.write(explanation)

# Run the prediction and explanation based on user input
if ticker:
    get_recommendation(ticker)
