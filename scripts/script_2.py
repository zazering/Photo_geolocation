# app/core/config.py - Конфигурация приложения
config_content = '''from functools import lru_cache
from typing import Optional, List
from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Photo Geolocation Service"
    version: str = "1.0.0"
    debug: bool = False
    
    host: str = "0.0.0.0"
    port: int = 8000
    
    database_url: str = Field(..., env="DATABASE_URL")
    redis_url: str = Field(..., env="REDIS_URL")
    
    google_cloud_credentials_path: Optional[str] = Field(None, env="GOOGLE_APPLICATION_CREDENTIALS")
    google_maps_api_key: Optional[str] = Field(None, env="GOOGLE_MAPS_API_KEY")
    
    locationiq_api_key: Optional[str] = Field(None, env="LOCATIONIQ_API_KEY")
    opencage_api_key: Optional[str] = Field(None, env="OPENCAGE_API_KEY")
    
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    max_file_size: int = 10 * 1024 * 1024
    allowed_extensions: List[str] = [".jpg", ".jpeg", ".png", ".webp", ".tiff"]
    upload_path: str = "uploads"
    
    cache_ttl: int = 3600
    
    landmark_confidence_threshold: float = 0.6
    geocoding_confidence_threshold: float = 0.7
    
    cors_origins: List[str] = ["*"]
    
    @validator("database_url")
    def validate_database_url(cls, v: str) -> str:
        if not v.startswith(("postgresql://", "sqlite:///")):
            raise ValueError("Database URL must be PostgreSQL or SQLite")
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
'''

with open("photo_geolocation/app/core/config.py", "w") as f:
    f.write(config_content)

print("✅ Конфигурация создана")