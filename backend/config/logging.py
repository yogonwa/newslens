from loguru import logger
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logger
logger.remove()  # Remove default handler

# Add console handler
logger.add(
    sys.stderr,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level=os.getenv("LOG_LEVEL", "INFO"),
    colorize=True,
)

# Add file handler if in production
if os.getenv("ENVIRONMENT") == "production":
    logger.add(
        "logs/app.log",
        rotation="500 MB",
        retention="10 days",
        level=os.getenv("LOG_LEVEL", "INFO"),
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    ) 