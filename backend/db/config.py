from typing import Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB Configuration
MONGO_CONFIG: Dict[str, Any] = {
    'host': os.getenv('MONGO_HOST', 'localhost'),
    'port': int(os.getenv('MONGO_PORT', 27017)),
    'database': os.getenv('MONGO_DB', 'newslens'),
    'username': os.getenv('MONGO_USER', ''),
    'password': os.getenv('MONGO_PASSWORD', ''),
}

# Collection Names
COLLECTIONS = {
    'sources': 'news_sources',
    'headlines': 'headlines'
}

# Index Configurations
INDEXES = {
    'headlines': [
        {'keys': [('source_id', 1), ('display_timestamp', -1)], 'name': 'source_time_idx'},
        {'keys': [('display_timestamp', -1)], 'name': 'time_idx'},
        {'keys': [('source_id', 1)], 'name': 'source_idx'},
        {'keys': [('status', 1)], 'name': 'status_idx'}
    ],
    'sources': [
        {'keys': [('active', 1)], 'name': 'active_idx'},
        {'keys': [('name', 1)], 'name': 'name_idx'}
    ]
} 