# Buy/Sell recommendation system
This project is an AI-powered Stock Recommendation System designed to provide actionable insights such as "Buy" or "Sell" recommendations for stocks. By integrating data from multiple sources, applying advanced machine learning techniques, and presenting a user-friendly interface, this system empowers users to make data-driven investment decisions.


**Features**
###### Smart Data Integration:

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
**How It Works**
###### Data Gathering:
The system fetches stock prices, technical indicators, and sentiment data from news articles and tweets.

###### Data Processing & Feature Engineering:

Calculates essential indicators like moving averages, Bollinger Bands, and RSI.
Performs sentiment analysis to assess market mood.
###### Model Training:

Trains a Random Forest Classifier on historical stock data combined with sentiment metrics.
Optimized for accurate predictions of stock trends, with cross-validated accuracy of over 85%.
###### Recommendation & Visualization:

Provides "Buy" or "Sell" predictions for selected stocks.
Visualizes key data points like stock prices, moving averages, and sentiment trends in real time.
**Example Use Case**

A user can:

Enter a stock ticker (e.g., AAPL or TSLA).
View the system's recommendation: "Buy" or "Sell".
Explore visualized trends such as moving averages, RSI, and historical price data.
Gain confidence in decision-making by checking sentiment analysis from news and Twitter.
###### Why You'll Love This
This system is perfect for anyone who:

Wants data-driven insights for their stock trades.
Values an easy-to-use interface to understand complex stock trends.
Aims to combine technical analysis with market sentiment for smarter investment decisions.
Whether you're a seasoned trader or a curious investor, this recommendation system will elevate your stock analysis game!