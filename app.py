import streamlit as st
from langchain_handler import generate_recommendation
from data_fetcher import fetch_stock_data
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

def display_stock_data(ticker):
    """
    Display stock data in the Streamlit app for a given ticker.
    """
    stock_history, stock_info = fetch_stock_data(ticker)

    st.subheader(f"Stock Data for {ticker}")
    st.write(f"Current Price: ${stock_info.get('currentPrice', 'N/A')}")
    st.write(f"1-Month Change: {stock_info.get('regularMarketChangePercent', 'N/A')}%")
    st.write(f"Volume: {stock_info.get('regularMarketVolume', 'N/A')}")
    st.write(f"P/E Ratio: {stock_info.get('trailingPE', 'N/A')}")
    st.write(f"52-Week Range: {stock_info.get('fiftyTwoWeekRange', 'N/A')}")

    # Show historical stock data (e.g., last 5 days)
    st.subheader("Recent Stock History (Last 5 Days)")
    st.write(stock_history.tail(5))

def display_recommendation(ticker):
    recommendation, explanation = generate_recommendation(ticker)
    
    # Display the stock ticker
    st.subheader(f"Stock Recommendation for {ticker}")
    
    # Display the recommendation and explanation
    st.write(f"**Recommendation**: {recommendation}")
    st.write(f"**Explanation**: {explanation}")


def app():
    st.title("LLM-based Stock Recommendation System")

    st.sidebar.header("Stock Ticker Input")
    ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL):")

    if ticker:
        display_stock_data(ticker)
        display_recommendation(ticker)
    else:
        st.write("Please enter a valid stock ticker in the sidebar.")


if __name__ == "__main__":
    app()
