import os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from backend.config import get_config

# Create FastAPI app
app = FastAPI(
    title="NewsLens API",
    description="API for extracting and analyzing news content",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers
from api.routes import health
app.include_router(health.router, prefix="/api/v1/health", tags=["health"])

config = get_config()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=getattr(config, "api_host", "0.0.0.0"),
        port=int(getattr(config, "api_port", 8000)),
        reload=getattr(config, "environment", "development") == "development",
    ) 