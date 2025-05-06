from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import health
from backend.api.routes import snapshots
from backend.config import get_config

# Load and validate environment variables
config = get_config()

# Create FastAPI app
app = FastAPI(
    title="NewsLens API",
    description="API for NewsLens news analysis platform",
    version="0.1.0",
    debug=config.environment == "development"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Optionally use config.cors_origins if you add it to config
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(snapshots.router)

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