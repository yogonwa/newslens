from datetime import datetime
from typing import List, Dict
from bson import ObjectId
from ..connection import db_connection
from ..models import SourceDocument, HeadlineDocument, SourceMetadata

# Initial news sources
NEWS_SOURCES = [
    {
        "name": "CNN",
        "url": "https://www.cnn.com",
        "metadata": {
            "user_agent": "NewsLensBot/0.1",
            "timezone": "America/New_York",
            "wayback_enabled": True,
            "live_scrape_enabled": True
        }
    },
    {
        "name": "Fox News",
        "url": "https://www.foxnews.com",
        "metadata": {
            "user_agent": "NewsLensBot/0.1",
            "timezone": "America/New_York",
            "wayback_enabled": True,
            "live_scrape_enabled": True
        }
    },
    {
        "name": "The New York Times",
        "url": "https://www.nytimes.com",
        "metadata": {
            "user_agent": "NewsLensBot/0.1",
            "timezone": "America/New_York",
            "wayback_enabled": True,
            "live_scrape_enabled": True
        }
    },
    {
        "name": "The Washington Post",
        "url": "https://www.washingtonpost.com",
        "metadata": {
            "user_agent": "NewsLensBot/0.1",
            "timezone": "America/New_York",
            "wayback_enabled": True,
            "live_scrape_enabled": True
        }
    },
    {
        "name": "USA Today",
        "url": "https://www.usatoday.com",
        "metadata": {
            "user_agent": "NewsLensBot/0.1",
            "timezone": "America/New_York",
            "wayback_enabled": True,
            "live_scrape_enabled": True
        }
    }
]

def seed_sources() -> List[ObjectId]:
    """Seed the database with initial news sources."""
    db = db_connection.db
    sources_collection = db['news_sources']
    
    # Clear existing sources
    sources_collection.delete_many({})
    
    # Insert new sources
    source_ids = []
    for source_data in NEWS_SOURCES:
        source = SourceDocument(**source_data)
        result = sources_collection.insert_one(source.dict())
        source_ids.append(result.inserted_id)
    
    print(f"Seeded {len(source_ids)} news sources")
    return source_ids

def seed_test_headlines(source_ids: List[ObjectId]):
    """Seed the database with test headlines."""
    db = db_connection.db
    headlines_collection = db['headlines']
    
    # Clear existing headlines
    headlines_collection.delete_many({})
    
    # Create test headlines for each source
    for source_id in source_ids:
        # Get source details
        source = db['news_sources'].find_one({'_id': source_id})
        if not source:
            continue
            
        # Create test headlines
        test_headlines = [
            {
                'text': f"Test Headline 1 for {source['name']}",
                'type': 'h1',
                'position': 1,
                'metadata': {
                    'is_breaking': True,
                    'editorial_tag': 'BREAKING'
                }
            },
            {
                'text': f"Test Headline 2 for {source['name']}",
                'type': 'h2',
                'position': 2,
                'metadata': {
                    'is_breaking': False
                }
            }
        ]
        
        # Create headline document
        headline_doc = HeadlineDocument(
            source_id=source_id,
            display_timestamp=datetime.utcnow(),
            actual_timestamp=datetime.utcnow(),
            headlines=test_headlines,
            screenshot={
                'url': f"https://example.com/screenshots/{source['name'].lower()}.png",
                'format': 'png',
                'size': 1000000,
                'dimensions': {'width': 1920, 'height': 1080}
            },
            metadata={
                'page_title': f"{source['name']} - Test Page",
                'url': source['url'],
                'user_agent': source['metadata']['user_agent'],
                'time_difference': 0,
                'confidence': 'high',
                'collection_method': 'test',
                'status': 'success'
            }
        )
        
        # Insert headline
        headlines_collection.insert_one(headline_doc.dict())
    
    print(f"Seeded test headlines for {len(source_ids)} sources")

def main():
    """Main seeding function."""
    print("Starting database seeding...")
    
    # Seed sources
    source_ids = seed_sources()
    
    # Seed test headlines
    seed_test_headlines(source_ids)
    
    print("Database seeding complete!")

if __name__ == "__main__":
    main() 