from typing import Dict, Optional, List
from datetime import datetime
from bson import ObjectId
import logging
from backend.db.models import HeadlineDocument, Screenshot, Headline, HeadlineMeta, DocumentHeadlineMetadata

class DBService:
    """
    Database service for handling MongoDB operations while maintaining existing schema
    """
    def __init__(self, db_client):
        self.db = db_client
        self.headlines = self.db.headlines
        self.sources = self.db.sources

    async def save_snapshot(
        self,
        source_id: ObjectId,
        display_timestamp: datetime,
        actual_timestamp: datetime,
        s3_url: str,
        wayback_url: str,
        headlines: List[Dict],
        image_meta: Dict
    ) -> ObjectId:
        """
        Save snapshot data maintaining existing schema structure
        """
        try:
            # Construct Screenshot object
            screenshot = Screenshot(
                url=s3_url,
                format="png",
                size=image_meta.get('size', 0),
                dimensions=image_meta.get('dimensions', {}),
                wayback_url=wayback_url
            )

            # Process headlines
            processed_headlines = []
            for idx, h in enumerate(headlines):
                headline_meta = None
                if any(key in h for key in ['editorial_tag', 'subheadline', 'article_url']):
                    headline_meta = HeadlineMeta(
                        editorial_tag=h.get('editorial_tag'),
                        subheadline=h.get('subheadline'),
                        article_url=h.get('url')
                    )

                processed_headlines.append(
                    Headline(
                        text=h.get('headline', ''),
                        type='main' if idx == 0 else 'secondary',
                        position=idx + 1,
                        metadata=headline_meta
                    )
                )

            # Construct metadata
            meta = DocumentHeadlineMetadata(
                page_title=h.get('page_title', ''),
                url=wayback_url,
                user_agent=h.get('user_agent', ''),
                time_difference=int((actual_timestamp - display_timestamp).total_seconds()),
                confidence="high",
                collection_method="wayback",
                status="success"
            )

            # Create document
            doc = HeadlineDocument(
                source_id=source_id,
                display_timestamp=display_timestamp,
                actual_timestamp=actual_timestamp,
                headlines=processed_headlines,
                screenshot=screenshot,
                metadata=meta
            )

            # Insert or update
            result = await self.headlines.update_one(
                {
                    "source_id": source_id,
                    "display_timestamp": display_timestamp
                },
                {"$set": doc.dict()},
                upsert=True
            )

            return result.upserted_id or doc.id

        except Exception as e:
            logging.error(f"Database operation failed: {e}")
            raise

    async def get_source_id(self, source_name: str) -> Optional[ObjectId]:
        """Get source ID by name"""
        source = await self.sources.find_one({"name": source_name})
        return source["_id"] if source else None

    async def check_existing_snapshot(
        self,
        source_id: ObjectId,
        display_timestamp: datetime
    ) -> bool:
        """Check if snapshot already exists"""
        exists = await self.headlines.find_one(
            {
                "source_id": source_id,
                "display_timestamp": display_timestamp
            },
            {"_id": 1}
        )
        return bool(exists) 