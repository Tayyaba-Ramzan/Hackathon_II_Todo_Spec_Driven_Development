from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from pydantic import Field

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    better_auth_secret: str = Field(default="Xp2Pai0rYqduM32JBoNYaqWYVQjZEIWk", alias="BETTER_AUTH_SECRET")
    database_url: str = Field(default="sqlite:///./test.db", alias="DATABASE_URL")  # Using SQLite for testing as default
    neon_db_url: Optional[str] = Field(default=None, alias="NEON_DB_URL")
    next_public_better_auth_url: Optional[str] = Field(default="http://localhost:3000", alias="NEXT_PUBLIC_BETTER_AUTH_URL")
    next_public_api_url: Optional[str] = Field(default="http://localhost:8000", alias="NEXT_PUBLIC_API_URL")

    model_config = SettingsConfigDict(env_file=".env", extra="allow")  # Allow extra fields to prevent validation errors

# Create a single instance of settings
settings = Settings()