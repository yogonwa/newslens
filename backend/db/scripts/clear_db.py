from backend.db import db_connection
from backend.config import get_config


def clear_collections():
    config = get_config()
    db = db_connection.db
    collections = config.mongodb['collections']
    
    for name in collections.values():
        collection = db[name]
        result = collection.delete_many({})
        print(f"Cleared {result.deleted_count} documents from collection '{name}'")

if __name__ == "__main__":
    clear_collections() 