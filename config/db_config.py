import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    def __init__(self):
        self.mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        self.database_name = os.getenv("DATABASE_NAME", "transaction_categorization")
        self.client = None
        self.db = None
    
    def connect(self):
        try:
            self.client = MongoClient(self.mongodb_uri)
            self.db = self.client[self.database_name]
            # Test connection
            self.client.server_info()
            return True
        except Exception as e:
            print(f"Database connection error: {e}")
            return False
    
    def get_database(self):
        if self.db is None:
            self.connect()
        return self.db
    
    def close(self):
        if self.client:
            self.client.close()

# Singleton instance
db_config = DatabaseConfig()