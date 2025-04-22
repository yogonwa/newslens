from typing import Optional
from pymongo import MongoClient
from pymongo.database import Database
from .config import MONGO_CONFIG

class MongoDBConnection:
    _instance: Optional['MongoDBConnection'] = None
    _client: Optional[MongoClient] = None
    _db: Optional[Database] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._client is None:
            self._connect()

    def _connect(self):
        """Establish connection to MongoDB."""
        try:
            # Construct connection string
            connection_string = f"mongodb://{MONGO_CONFIG['host']}:{MONGO_CONFIG['port']}"
            
            # Add authentication if credentials are provided
            if MONGO_CONFIG['username'] and MONGO_CONFIG['password']:
                connection_string = f"mongodb://{MONGO_CONFIG['username']}:{MONGO_CONFIG['password']}@{MONGO_CONFIG['host']}:{MONGO_CONFIG['port']}"
            
            self._client = MongoClient(connection_string)
            self._db = self._client[MONGO_CONFIG['database']]
            print(f"Connected to MongoDB at {MONGO_CONFIG['host']}:{MONGO_CONFIG['port']}")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise

    @property
    def db(self) -> Database:
        """Get database instance."""
        if self._db is None:
            self._connect()
        return self._db

    def close(self):
        """Close the MongoDB connection."""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None

# Create a singleton instance
db_connection = MongoDBConnection() 