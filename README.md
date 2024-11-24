# Buy/Sell recommendation system
This project is an AI-powered Stock Recommendation System designed to provide actionable insights such as "Buy" or "Sell" recommendations for stocks. By integrating data from multiple sources, applying advanced machine learning techniques, and presenting a user-friendly interface, this system empowers users to make data-driven investment decisions.


**Features**
Smart Data Integration:

Yahoo Finance API: Provides historical stock data.
News API: Delivers news articles for sentiment analysis.
Twitter API: Captures real-time social sentiment about stocks.
Alpha Vantage API: Supplies additional technical indicators for deeper analysis.
Machine Learning for Predictions:

Predicts stock movements using a Random Forest Classifier trained on historical data and technical indicators.
Combines financial indicators (e.g., RSI, moving averages) with sentiment analysis for a holistic view.
Interactive UI with Streamlit:

User-friendly interface to explore stock trends, visualize technical indicators, and get "Buy" or "Sell" recommendations.
Offers interactive charts and insights to help users quickly analyze stock performance.
###### Data Storage:

Uses PostgreSQL to store fetched data, ensuring fast and scalable access to historical and real-time datasets.
