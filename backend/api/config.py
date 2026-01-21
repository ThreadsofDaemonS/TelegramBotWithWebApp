"""API configuration using pydantic-settings."""
import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class APIConfig(BaseSettings):
    """API configuration settings."""
    
    # Bot settings
    bot_token: str = os.getenv("BOT_TOKEN", "")
    
    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://taskbot:changeme@localhost:5432/tasktracker")
    
    # API settings
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost")
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


# Create global config instance
config = APIConfig()
