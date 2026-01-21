"""Bot configuration using pydantic-settings."""
import os
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class BotConfig(BaseSettings):
    """Bot configuration settings."""
    
    # Bot settings
    bot_token: str = os.getenv("BOT_TOKEN", "")
    webapp_url: str = os.getenv("WEBAPP_URL", "http://localhost")  # WebApp URL for buttons
    
    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://taskbot:changeme@localhost:5432/tasktracker")
    
    # Redis settings
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


# Create global config instance
config = BotConfig()
