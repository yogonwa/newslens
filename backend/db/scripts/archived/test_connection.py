# (archived) This script is no longer used in the main pipeline, kept for reference.

from pymongo import MongoClient
from dotenv import load_dotenv
import os
from pathlib import Path

def test_connection():
    # Get absolute path to .env file
    env_path = Path(__file__).resolve().parents[2] / '.env'
    print(f"Looking for .env file at: {env_path}")
    
    # Load environment variables
    load_dotenv(env_path)
    
    # Get MongoDB URI from environment
    mongo_uri = os.getenv('MONGO_URI')
    
    # Print connection string (with sensitive info redacted)
    if mongo_uri:
        redacted_uri = mongo_uri.replace(mongo_uri.split('@')[0], 'mongodb+srv://***:***')
        print(f"Attempting to connect with URI: {redacted_uri}")
    else:
        print("MONGO_URI not found in environment variables")
        return
    
    try:
        # Create a new client and connect to the server
        client = MongoClient(mongo_uri)
        
        # Send a ping to confirm a successful connection
        client.admin.command('ping')
        print("Successfully connected to MongoDB Atlas!")
        
        # List all databases
        print("\nAvailable databases:")
        for db in client.list_database_names():
            print(f"- {db}")
            
        # Close the connection
        client.close()
        
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}") 