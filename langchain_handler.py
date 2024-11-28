from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from data_fetcher import fetch_stock_data, fetch_financial_data, fetch_stock_news
import os
from langchain.llms import OpenAI 

llm = OpenAI(api_key="OPENAI_KEY")

def generate_recommendation(ticker):
    stock_history, stock_info = fetch_stock_data(ticker)

    if stock_info is None:
        return "Error: No stock info available", "Could not fetch data for the given ticker."

    # Check if 'currentPrice' is in stock_info
    if 'currentPrice' in stock_info:
        price = stock_info['currentPrice']  # Directly access the 'currentPrice' key
    else:
        return "Error: Missing 'currentPrice'", f"The stock data for {ticker} does not contain the 'currentPrice'."

    # You can also fetch other useful data from stock_info
    pe_ratio = stock_info.get('trailingPE', 'N/A')  # Use 'N/A' if P/E ratio is not available
    market_cap = stock_info.get('marketCap', 'N/A')

    # Fetching financial data
    financial_data = fetch_financial_data(ticker)
    
    # Fetching the stock news data
    news_data_list = fetch_stock_news(ticker)

    # Handle news data and extract sentiment
    if isinstance(news_data_list, list) and news_data_list:
        sentiment = "Positive" if "positive" in news_data_list[0].get('title', '').lower() else "Negative"
    else:
        sentiment = "No Sentiment Data"

    # Define the prompt to send to the model
    prompt = f"""
    You are a stock recommendation expert. Use the following data to provide a recommendation on whether the stock should be a "Buy", "Sell", or "Hold":

    Stock Data: 
    - Price: ${price}
    - P/E Ratio: {pe_ratio}
    - Market Cap: {market_cap}

    News Sentiment: {sentiment}

    Based on these inputs, recommend whether the stock is a "Buy", "Sell", or "Hold". Provide an explanation.
    """

    # Assuming you are using a simple function to call the model and get the result
    llm_chain = LLMChain(prompt=PromptTemplate(input_variables=["input"], template=prompt), llm=llm)

    # Generate the recommendation from the model
    result = llm_chain.run({'input': prompt})

    # Parse the result to extract recommendation and explanation
    recommendation = parse_recommendation(result)
    explanation = parse_explanation(result)

    return recommendation, explanation

# Helper functions to parse the recommendation and explanation
def parse_recommendation(result):
    if "buy" in result.lower():
        return "Buy"
    elif "sell" in result.lower():
        return "Sell"
    elif "hold" in result.lower():
        return "Hold"
    else:
        return "Hold"  # Default to "Hold" if uncertain

def parse_explanation(result):
    # You can clean up or format the result for explanation if necessary
    return result

# Example of usage (for testing purposes)
if __name__ == "__main__":
    ticker = "AAPL"
    recommendation, explanation = generate_recommendation(ticker)
    print(f"Recommendation: {recommendation}")
    print(f"Explanation: {explanation}")
