from typing import List, Dict, Any, Optional
from datetime import datetime
from bson import ObjectId
from pymongo.collection import Collection
from .connection import db_connection
from .config import COLLECTIONS, INDEXES
from .models import HeadlineDocument, SourceDocument

class DatabaseOperations:
    def __init__(self):
        self.db = db_connection.db
        self._setup_collections()
        self._create_indexes()

    def _setup_collections(self):
        """Initialize collections if they don't exist."""
        self.sources: Collection = self.db[COLLECTIONS['sources']]
        self.headlines: Collection = self.db[COLLECTIONS['headlines']]

    def _create_indexes(self):
        """Create indexes for collections."""
        # Create indexes for headlines collection
        for index in INDEXES['headlines']:
            self.headlines.create_index(index['keys'], name=index['name'])

        # Create indexes for sources collection
        for index in INDEXES['sources']:
            self.sources.create_index(index['keys'], name=index['name'])

    # Source Operations
    def add_source(self, source: SourceDocument) -> ObjectId:
        """Add a new news source."""
        result = self.sources.insert_one(source.dict())
        return result.inserted_id

    def get_source(self, source_id: ObjectId) -> Optional[Dict[str, Any]]:
        """Get a news source by ID."""
        return self.sources.find_one({'_id': source_id})

    def update_source(self, source_id: ObjectId, update_data: Dict[str, Any]) -> bool:
        """Update a news source."""
        result = self.sources.update_one(
            {'_id': source_id},
            {'$set': update_data}
        )
        return result.modified_count > 0

    def list_sources(self, active_only: bool = True) -> List[Dict[str, Any]]:
        """List all news sources."""
        query = {'active': True} if active_only else {}
        return list(self.sources.find(query))

    # Headline Operations
    def add_headline(self, headline: HeadlineDocument) -> ObjectId:
        """Add a new headline document."""
        result = self.headlines.insert_one(headline.dict())
        return result.inserted_id

    def get_headlines_by_time(self, 
                            start_time: datetime, 
                            end_time: datetime,
                            source_ids: Optional[List[ObjectId]] = None) -> List[Dict[str, Any]]:
        """Get headlines within a time range."""
        query = {
            'display_timestamp': {
                '$gte': start_time,
                '$lte': end_time
            }
        }
        if source_ids:
            query['source_id'] = {'$in': source_ids}
        return list(self.headlines.find(query))

    def get_headlines_by_source(self, 
                              source_id: ObjectId,
                              limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent headlines for a specific source."""
        return list(self.headlines.find(
            {'source_id': source_id}
        ).sort('display_timestamp', -1).limit(limit))

    def update_headline(self, 
                       headline_id: ObjectId, 
                       update_data: Dict[str, Any]) -> bool:
        """Update a headline document."""
        result = self.headlines.update_one(
            {'_id': headline_id},
            {'$set': update_data}
        )
        return result.modified_count > 0

    def delete_headline(self, headline_id: ObjectId) -> bool:
        """Delete a headline document."""
        result = self.headlines.delete_one({'_id': headline_id})
        return result.deleted_count > 0

# Create a singleton instance
db_ops = DatabaseOperations() 