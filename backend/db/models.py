from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId

class HeadlineMeta(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    font_size: Optional[str] = None
    color: Optional[str] = None
    is_breaking: bool = False
    editorial_tag: Optional[str] = None
    subheadline: Optional[str] = None
    article_url: Optional[str] = None

class Headline(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    text: str
    type: str
    position: int
    sentiment: Optional[float] = None
    metadata: Optional[HeadlineMeta] = None

class Screenshot(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    url: str
    format: str
    size: int
    dimensions: Dict[str, int]
    wayback_url: Optional[str] = None

class DocumentHeadlineMetadata(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
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
    model_config = ConfigDict(arbitrary_types_allowed=True)
    short_id: str  # Canonical, human-readable source key (e.g., 'cnn', 'foxnews')
    display_timestamp: datetime
    actual_timestamp: datetime
    headlines: List[Headline]
    screenshot: Screenshot
    metadata: DocumentHeadlineMetadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class SourceMetadata(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    screenshot_path: Optional[str] = None
    last_updated: Optional[datetime] = None
    timezone: str = "America/New_York"
    user_agent: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    wayback_enabled: bool = True
    live_scrape_enabled: bool = True

class SourceDocument(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str
    url: str
    active: bool = True
    metadata: SourceMetadata 