import pandas as pd
import psycopg2
from newsapi import NewsApiClient

# Your valid API key from NewsAPI
newsapi = NewsApiClient(api_key='6c0c2ea412374febbe8f03e6926bf06f')

# Database connection parameters
DB_HOST = 'database-1.cj4qwuksc2n1.eu-north-1.rds.amazonaws.com'
DB_NAME = ''
DB_USER = 'postgres'
DB_PASSWORD = 'mypassword'
DB_PORT = '5432'  # Default PostgreSQL port

# List of company keywords to search for
list1 = ["Tesla", "Apple", "Microsoft", "Amazon", "Meta"]

# Function to fetch news articles and store in both CSV and PostgreSQL
def fetch_and_store_news():
    for company in list1:
        # Using the client library to get articles related to each company
        all_articles = newsapi.get_everything(
            q=company,  # Searching for the company keyword
            language='en',  # English articles
            from_param='2024-10-16',  # Start date
            to='2024-12-16',  # End date
            sort_by='relevancy'  # Sort by relevance
        )

        # Convert the response to a DataFrame
        df = pd.DataFrame.from_dict(all_articles)

        # Assign the company keyword as a group label
        df = df.assign(Group=company)
        
        # Extract articles content into a new DataFrame
        df1 = df.articles.apply(pd.Series)
        
        # Extract source details into a new DataFrame
        df2 = df1.source.apply(pd.Series)
        
        # Concatenate all data, drop unnecessary columns, and rearrange
        df3 = pd.concat([df, df1, df2], axis=1).drop(
            ['urlToImage', 'name', 'id', 'articles', 'source', 'status', 'totalResults'], axis=1
        )
        
        # Rearranging columns for final DataFrame
        df3 = df3[['Group', 'publishedAt', 'author', 'url', 'title', 'description', 'content']]
        
        # Save to CSV file
        df3.to_csv('newsdata.csv', mode='a', header=False, index=False)
        
        # Save to PostgreSQL
        store_articles_in_db(df3)
        
        print(f"Articles for {company} fetched and saved.")

# Function to store the articles in PostgreSQL database
def store_articles_in_db(df):
    try:
        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        cursor = conn.cursor()

        # Create table if not exists (You can adjust this schema based on your needs)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS news_article (
                id SERIAL PRIMARY KEY,
                group_name TEXT,
                published_at TIMESTAMP,
                author TEXT,
                url TEXT,
                title TEXT,
                description TEXT,
                content TEXT
            )
        """)
        conn.commit()

        # Insert data into the database
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO news_article (group_name, published_at, author, url, title, description, content)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                row['Group'],
                row['publishedAt'],
                row['author'],
                row['url'],
                row['title'],
                row['description'],
                row['content']
            ))

        conn.commit()
        print(f"Successfully inserted articles into the database.")
        
        # Close the cursor and connection
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error inserting data into the database: {e}")

# Fetch and store the news articles
fetch_and_store_news()
