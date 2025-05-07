import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file in project root
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import get_config
from backend.api.routes import health
from backend.api.routes import snapshots
from backend.api.routes import sources

"""
backend/main.py

This is the single entrypoint for the NewsLens FastAPI backend server.
- Serves all API endpoints (e.g., /api/snapshots, /api/v1/health)
- Handles CORS and app configuration
- Should NOT be confused with main_scraper.py, which is the CLI pipeline for scraping and data ingestion.
"""

# Create FastAPI app
app = FastAPI(
    title="NewsLens API",
    description="API for extracting and analyzing news content",
    version="0.1.0",
)

# Configure CORS for all origins (adjust for production as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all API routers
app.include_router(health.router, prefix="/api/v1/health", tags=["health"])
app.include_router(snapshots.router, prefix="/api")
app.include_router(sources.router, prefix="/api")

# Root endpoint for basic health/info
@app.get("/")
def root():
    """Root endpoint for API status and version info."""
    return {"message": "Welcome to NewsLens API", "version": "0.1.0", "status": "running"}

# Load config for use in __main__ block
config = get_config()

if __name__ == "__main__":
    # For local development: run with `python backend/main.py` or via uvicorn
    import uvicorn
    uvicorn.run(
        "main:app",
        host=getattr(config, "api_host", "0.0.0.0"),
        port=int(getattr(config, "api_port", 8000)),
        reload=getattr(config, "environment", "development") == "development",
    ) 