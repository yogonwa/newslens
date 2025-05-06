"""
Configuration Package
"""

from typing import Optional
from .base import BaseConfig, DEFAULT_CAPTURE_TIMES, SOURCES

_config_instance: Optional[BaseConfig] = None

def get_config() -> BaseConfig:
    """
    Get the global configuration instance.
    Initializes configuration on first call.
    
    Returns:
        BaseConfig: The global configuration instance
    
    Raises:
        ConfigurationError: If required environment variables are missing or invalid
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = BaseConfig()
    return _config_instance 