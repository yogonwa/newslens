from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Optional
from backend.db.operations import db_ops

router = APIRouter()

class SourceOut(BaseModel):
    id: str = Field(..., alias="_id")
    short_id: str
    name: str
    color: str
    logo_url: Optional[str]
    website: Optional[str]
    region: Optional[str]

@router.get("/sources", response_model=List[SourceOut])
def get_sources():
    sources = list(db_ops.sources.find({}))
    # Convert ObjectId to str for _id
    for src in sources:
        src["_id"] = str(src["_id"])
    return sources 