

from functools import lru_cache
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

import os

def resolve_env_file() -> str:
    """
    Determine which .env file to load.
    Priority:
    1. If container injects MODE (e.g., MODE=prod) → .env.prod
    2. Else fallback to `.env.dev`
    """
    mode = os.getenv("MODE", "dev").lower().strip()

    # Ensure only valid modes are allowed
    allowed = {"dev", "development", "prod", "production", "staging"}
    if mode not in allowed:
        mode = "dev"

    return f".env.{mode}"
ENV_FILE = resolve_env_file()

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = "holehe-service"
    APP_VERSION: str = "2.0.0"
    MODE: str = Field(default="development", description="Application mode: development, staging, production")
    DEBUG: bool = Field(default=False, description="Enable debug mode")
    
    # API
    API_V1_PREFIX: str = "/api/v2"
    WORKERS: int = Field(default=2, description="Number of worker processes")
    
    # HTTP Client
    HTTP_TIMEOUT: int = Field(default=50, description="HTTP request timeout in seconds")
    HTTP_VERIFY_SSL: bool = Field(default=True, description="Verify SSL certificates")
    MAX_CONCURRENT_REQUESTS: int = Field(default=50, description="Maximum concurrent module requests")
    
    # Validator Service (Optional)
    VALIDATOR_URL: Optional[str] = Field(default=None, description="URL for validator service")
    VALIDATOR_ENABLED: bool = Field(default=False, description="Enable validator integration")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - [%(levelname)s] - %(message)s",
        description="Log format string"
    )
    

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Returns:
        Settings: Application settings
    """
    return Settings()