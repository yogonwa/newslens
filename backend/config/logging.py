from loguru import logger
import sys
from backend.config import get_config
import os

config = get_config()

logger.remove()  # Remove default handler

logger.add(
    sys.stderr,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level=getattr(config, 'log_level', os.getenv('LOG_LEVEL', 'INFO')),
    colorize=True,
)

if getattr(config, 'environment', os.getenv('ENVIRONMENT')) == "production":
    logger.add(
        "logs/app.log",
        rotation="500 MB",
        retention="10 days",
        level=getattr(config, 'log_level', os.getenv('LOG_LEVEL', 'INFO')),
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    ) 