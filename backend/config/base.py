from typing import Dict, Any
import os
from pathlib import Path
from dotenv import load_dotenv

class ConfigurationError(Exception):
    """Raised when configuration is invalid"""
    pass

class BaseConfig:
    """Base configuration class that loads and validates environment variables"""
    
    REQUIRED_VARS = {
        # MongoDB
        'MONGO_URI': str,
        'MONGO_DB': str,
        
        # AWS/S3
        'AWS_ACCESS_KEY_ID': str,
        'AWS_SECRET_ACCESS_KEY': str,
        'AWS_DEFAULT_REGION': str,
        'S3_BUCKET_NAME': str,
        
        # Scraper
        'USER_AGENT': str
    }
    
    def __init__(self):
        # Load environment variables
        # env_file = Path('.env')
        # if env_file.exists():
        #     load_dotenv(env_file)
            
        # Validate required variables
        self._validate_env()
        
        # Initialize sub-configurations
        self.mongodb = self._init_mongodb_config()
        self.s3 = self._init_s3_config()
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.environment = os.getenv('ENVIRONMENT', 'development')
        
    def _validate_env(self):
        """Validate all required environment variables are present and of correct type"""
        missing = []
        invalid = []
        
        for var, expected_type in self.REQUIRED_VARS.items():
            value = os.getenv(var)
            if value is None:
                missing.append(var)
            elif not isinstance(value, expected_type):
                invalid.append(f"{var} (expected {expected_type.__name__})")
                
        if missing or invalid:
            errors = []
            if missing:
                errors.append(f"Missing required variables: {', '.join(missing)}")
            if invalid:
                errors.append(f"Invalid variable types: {', '.join(invalid)}")
            raise ConfigurationError('\n'.join(errors))
    
    def _init_mongodb_config(self) -> Dict[str, Any]:
        """Initialize MongoDB configuration"""
        return {
            'uri': os.getenv('MONGO_URI'),
            'database': os.getenv('MONGO_DB'),
            'collections': {
                'sources': 'news_sources',
                'headlines': 'headlines'
            },
            'indexes': {
                'headlines': [
                    {'keys': [('display_timestamp', -1)], 'name': 'time_idx'},
                    {'keys': [('short_id', 1)], 'name': 'short_id_idx'},
                    {'keys': [('status', 1)], 'name': 'status_idx'}
                ],
                'sources': [
                    {'keys': [('active', 1)], 'name': 'active_idx'},
                    {'keys': [('name', 1)], 'name': 'name_idx'}
                ]
            }
        }
    
    def _init_s3_config(self) -> Dict[str, Any]:
        """Initialize S3 configuration"""
        return {
            'access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
            'secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
            'region': os.getenv('AWS_DEFAULT_REGION'),
            'bucket': os.getenv('S3_BUCKET_NAME'),
            'storage_structure': {
                'root': 'auto',
                'date_format': '%Y-%m-%d',
                'filename_format': '{source_key}_{time}.png'
            }
        }

DEFAULT_CAPTURE_TIMES = [
    "06:00",
    "09:00",
    "12:00",
    "15:00",
    "18:00"
]

SOURCES = [
    {
        "name": "CNN",
        "url": "https://www.cnn.com",
        "key": "cnn.com",
        "id": "cnn",
        "short_id": "cnn"
    },
    {
        "name": "Fox News",
        "url": "https://www.foxnews.com",
        "key": "foxnews.com",
        "id": "foxnews",
        "short_id": "foxnews"
    },
    {
        "name": "New York Times",
        "url": "https://www.nytimes.com",
        "key": "nytimes.com",
        "id": "nytimes",
        "short_id": "nytimes"
    },
    {
        "name": "Washington Post",
        "url": "https://www.washingtonpost.com",
        "key": "washingtonpost.com",
        "id": "washingtonpost",
        "short_id": "washingtonpost"
    },
    {
        "name": "USA Today",
        "url": "https://www.usatoday.com",
        "key": "usatoday.com",
        "id": "usatoday",
        "short_id": "usatoday"
    }
] 