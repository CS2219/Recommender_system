import tweepy
import csv
from datetime import datetime
import time

# Set up authentication
client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAADAIxAEAAAAAjbneOXHwkQac%2FNQpIXyHGDUhu%2Fs%3D4tNqvp7NDqAz6CpMoH3rRANGVyawUrCrXSVtj6SuihWnkTvhZR')

def get_tweets(keywords, start_date):
    # Set the number of tweets you want to retrieve
    number_of_tweets = 100

    # Convert start_date to datetime format
    start_time = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")

    # Get tweets based on keywords using the new search method for v2
    tweets_for_csv = []
    try:
        for tweet in tweepy.Paginator(client.search_recent_tweets, query=keywords, tweet_fields=["created_at", "text"], start_time=start_time, max_results=10).flatten(limit=number_of_tweets):
            tweets_for_csv.append([tweet.id, tweet.created_at, tweet.text])

        # Write the tweets to a CSV file
        outfile = keywords.replace(" ", "_") + "_tweets.csv"
        print(f"Writing tweets to {outfile}")
        with open(outfile, 'w+', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(["Tweet ID", "Created At", "Tweet Text"])  # CSV header
            writer.writerows(tweets_for_csv)

    except tweepy.errors.TooManyRequests as e:
        print("Rate limit exceeded. Waiting for 15 minutes.")
        time.sleep(120)  # Sleep for 15 minutes before retrying
        get_tweets(keywords, start_date)

# If we're running this as a script
if __name__ == '__main__':
    # List of companies or stock symbols
    company_list = ['Tesla', 'Apple', 'Microsoft', 'Amazon', 'Google', 'Meta', 'NVIDIA']
    start_date = "2024-11-16T00:00:00"  # Fetch tweets after this date

    # Get tweets for each company name or stock symbol
    for company in company_list:
        get_tweets(company, start_date)  # Scrape tweets related to each company