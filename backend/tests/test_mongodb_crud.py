import pytest
from backend.db.operations import db_ops
from backend.db.models import HeadlineDocument, Headline, Screenshot, DocumentHeadlineMetadata
from datetime import datetime
from bson import ObjectId

@pytest.fixture(autouse=True)
def cleanup_headlines():
    # Cleanup before and after each test
    db_ops.headlines.delete_many({"test_marker": True})
    yield
    db_ops.headlines.delete_many({"test_marker": True})

def make_test_doc():
    return HeadlineDocument(
        short_id="cnn",
        source_id="cnn",
        display_timestamp=datetime.utcnow(),
        actual_timestamp=datetime.utcnow(),
        headlines=[
            Headline(text="Test headline", type="main", position=1)
        ],
        screenshot=Screenshot(
            url="test/url.png",
            format="png",
            size=12345,
            dimensions={"width": 1920, "height": 1080},
            wayback_url="https://web.archive.org/web/20250101000000/https://www.cnn.com/"
        ),
        metadata=DocumentHeadlineMetadata(
            page_title="Test Page",
            url="https://example.com",
            user_agent="TestAgent",
            time_difference=0,
            confidence="high",
            collection_method="test",
            status="success"
        ),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        # Add a marker for cleanup
        test_marker=True
    )

def test_crud_headline_document():
    doc = make_test_doc()
    inserted_id = db_ops.add_headline(doc)
    assert inserted_id is not None
    # Retrieve
    found = db_ops.headlines.find_one({"_id": inserted_id})
    assert found is not None
    assert found["screenshot"]["url"] == "test/url.png"
    # Update
    db_ops.update_headline(inserted_id, {"screenshot.url": "test/updated.png"})
    updated = db_ops.headlines.find_one({"_id": inserted_id})
    assert updated["screenshot"]["url"] == "test/updated.png"
    # Delete
    deleted = db_ops.delete_headline(inserted_id)
    assert deleted
    assert db_ops.headlines.find_one({"_id": inserted_id}) is None

def test_schema_validation():
    doc = make_test_doc()
    # Should not raise
    doc_dict = doc.dict()
    assert "short_id" in doc_dict
    assert "headlines" in doc_dict
    assert isinstance(doc_dict["headlines"], list) 