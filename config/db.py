from pymongo import MongoClient

# Replace with your actual MongoDB Atlas connection string
connection_string = "mongodb+srv://admin:admin@cluster0.2etwk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(connection_string)

# Create or connect to a database and collection
try:
    # Create a MongoDB client
    client = MongoClient(connection_string)
    
    # Ping the server to test the connection
    client.admin.command('ping')
    
    # Create or connect to a database and collection
    db = client['stock_recommendation']
    collection = db['stock_data']
    
    print("Connected to MongoDB Atlas successfully")

except ConnectionError as e:
    print(f"Failed to connect to MongoDB Atlas: {e}")