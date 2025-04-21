from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yaml
import os
from pathlib import Path

# Load configuration
config_path = Path(__file__).parent.parent / "config" / "development.yaml"
with open(config_path) as f:
    config = yaml.safe_load(f)

# Create FastAPI app
app = FastAPI(
    title="NewsLens API",
    description="API for NewsLens news analysis platform",
    version="0.1.0",
    debug=config["api"]["debug"]
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config["api"]["cors_origins"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to NewsLens API",
        "version": "0.1.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 