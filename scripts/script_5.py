# app/models/database.py - SQLAlchemy модели
database_models_content = '''from sqlalchemy import String, Integer, Float, Boolean, Text, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional, Dict, Any

from app.core.database import Base


class ProcessingLog(Base):
    __tablename__ = "processing_logs"
    
    request_id: Mapped[str] = mapped_column(String(36), unique=True, index=True)
    filename: Mapped[str] = mapped_column(String(255))
    file_size_bytes: Mapped[int] = mapped_column(Integer)
    
    processing_mode: Mapped[str] = mapped_column(String(20))
    processing_time_ms: Mapped[int] = mapped_column(Integer)
    success: Mapped[bool] = mapped_column(Boolean, default=False)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    hypotheses_count: Mapped[int] = mapped_column(Integer, default=0)
    best_confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    best_source: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    best_latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    best_longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    apis_used: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    landmark_results: Mapped[int] = mapped_column(Integer, default=0)
    text_results: Mapped[int] = mapped_column(Integer, default=0)
    geocoding_queries: Mapped[int] = mapped_column(Integer, default=0)
    
    has_exif_gps: Mapped[bool] = mapped_column(Boolean, default=False)
    camera_make: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    camera_model: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    datetime_taken: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class APIUsageLog(Base):
    __tablename__ = "api_usage_logs"
    
    api_name: Mapped[str] = mapped_column(String(50), index=True)
    endpoint: Mapped[str] = mapped_column(String(255))
    request_count: Mapped[int] = mapped_column(Integer, default=1)
    success_count: Mapped[int] = mapped_column(Integer, default=0)
    error_count: Mapped[int] = mapped_column(Integer, default=0)
    total_response_time_ms: Mapped[int] = mapped_column(Integer, default=0)
    date: Mapped[datetime] = mapped_column(DateTime, index=True)


class CacheEntry(Base):
    __tablename__ = "cache_entries"
    
    cache_key: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    value: Mapped[Dict[str, Any]] = mapped_column(JSON)
    expires_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    hit_count: Mapped[int] = mapped_column(Integer, default=0)
    last_accessed: Mapped[datetime] = mapped_column(DateTime)


class UserSession(Base):
    __tablename__ = "user_sessions"
    
    session_id: Mapped[str] = mapped_column(String(36), unique=True, index=True)
    ip_address: Mapped[str] = mapped_column(String(45))
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    requests_count: Mapped[int] = mapped_column(Integer, default=0)
    last_request_at: Mapped[datetime] = mapped_column(DateTime)
'''

with open("photo_geolocation/app/models/database.py", "w") as f:
    f.write(database_models_content)

print("✅ SQLAlchemy модели созданы")