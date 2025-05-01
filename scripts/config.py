from typing import Dict, List
import os
from pathlib import Path

class Config:
    # S3 Configuration
    S3_BUCKET = os.getenv('S3_BUCKET', 'newslens-screenshots')
    
    # MongoDB Configuration
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
    MONGO_DB = os.getenv('MONGO_DB', 'newslens')
    
    # Screenshot Configuration
    VIEWPORT = {
        "width": 1920,
        "height": 2000,
        "device_scale_factor": 2.0
    }
    
    # Default time slots
    DEFAULT_TIMES = ["06:00", "09:00", "12:00", "15:00", "18:00"]
    
    # News sources configuration
    NEWS_SOURCES: List[Dict] = [
        {"name": "CNN", "url": "https://www.cnn.com", "key": "cnn.com"},
        {"name": "Fox News", "url": "https://www.foxnews.com", "key": "foxnews.com"},
        {"name": "The New York Times", "url": "https://www.nytimes.com", "key": "nytimes.com"},
        {"name": "The Washington Post", "url": "https://www.washingtonpost.com", "key": "washingtonpost.com"},
        {"name": "USA Today", "url": "https://www.usatoday.com", "key": "usatoday.com"}
    ]
    
    # Wayback Machine Configuration
    WAYBACK_CDX_API = "https://web.archive.org/cdx/search/cdx"
    WAYBACK_BASE = "https://web.archive.org/web/"
    WAYBACK_USER_AGENT = "NewsLensBot/1.0 (+https://github.com/yourusername/newslens)"
    WAYBACK_CDX_PARAMS = {
        "output": "json",
        "filter": "statuscode:200",
        "collapse": "digest"
    }
    
    # User agent for requests
    USER_AGENT = "NewsLensBot/1.0 (+https://newslens.example.com)"
    
    # Retry configuration
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # seconds
    MAX_CONSECUTIVE_ERRORS = 3
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    
    @classmethod
    def load_env(cls, env_file: Path = None):
        """Load environment variables from .env file"""
        if env_file and env_file.exists():
            from dotenv import load_dotenv
            load_dotenv(env_file) 