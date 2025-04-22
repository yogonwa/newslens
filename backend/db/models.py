from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from bson import ObjectId

class HeadlineMetadata(BaseModel):
    font_size: Optional[str] = None
    color: Optional[str] = None
    is_breaking: bool = False
    editorial_tag: Optional[str] = None
    subheadline: Optional[str] = None
    article_url: Optional[str] = None

class Headline(BaseModel):
    text: str
    type: str
    position: int
    sentiment: Optional[float] = None
    metadata: Optional[HeadlineMetadata] = None

class Screenshot(BaseModel):
    url: str
    format: str
    size: int
    dimensions: Dict[str, int]
    wayback_url: Optional[str] = None

class HeadlineMetadata(BaseModel):
    page_title: str
    url: str
    wayback_url: Optional[str] = None
    user_agent: str
    time_difference: int
    confidence: str
    collection_method: str
    status: str
    error_message: Optional[str] = None
    original_timestamp: Optional[datetime] = None

class HeadlineDocument(BaseModel):
    source_id: ObjectId
    display_timestamp: datetime
    actual_timestamp: datetime
    headlines: List[Headline]
    screenshot: Screenshot
    metadata: HeadlineMetadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class SourceMetadata(BaseModel):
    screenshot_path: Optional[str] = None
    last_updated: Optional[datetime] = None
    timezone: str = "America/New_York"
    user_agent: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    wayback_enabled: bool = True
    live_scrape_enabled: bool = True

class SourceDocument(BaseModel):
    name: str
    url: str
    active: bool = True
    metadata: SourceMetadata 