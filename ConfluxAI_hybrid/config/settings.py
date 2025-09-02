"""
Configuration settings for ConfluxAI Multi-Modal Search Agent
"""
import os
from pathlib import Path
from typing import List

class Settings:
    """Application settings"""
    
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # File handling settings
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "50")) * 1024 * 1024  # 50MB default
    ALLOWED_EXTENSIONS: List[str] = [
        ".pdf", ".txt", ".docx", ".doc", 
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff",
        ".csv", ".xlsx", ".xls",
        ".pptx", ".ppt", ".html", ".htm", ".md", ".markdown",
        ".py", ".js", ".java", ".cpp", ".c", ".h", ".json", ".xml", ".rtf"
    ]
    
    # Storage settings
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")
    INDEX_DIR: str = os.getenv("INDEX_DIR", "indexes")
    
    # Vector database settings
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    VECTOR_DIM: int = int(os.getenv("VECTOR_DIM", "384"))
    INDEX_NAME: str = os.getenv("INDEX_NAME", "conflux_index")
    
    # Search settings
    DEFAULT_SEARCH_LIMIT: int = int(os.getenv("DEFAULT_SEARCH_LIMIT", "10"))
    DEFAULT_SIMILARITY_THRESHOLD: float = float(os.getenv("DEFAULT_SIMILARITY_THRESHOLD", "0.7"))
    
    # Text processing settings
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "512"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "50"))
    
    # Image processing settings
    IMAGE_ANALYSIS_MODEL: str = os.getenv("IMAGE_ANALYSIS_MODEL", "clip-ViT-B-32")
    MAX_IMAGE_SIZE: tuple = (1024, 1024)  # Max width, height
    
    # Database settings (PostgreSQL/Supabase)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:password@localhost:5432/conflux_ai")
    DATABASE_POOL_SIZE: int = int(os.getenv("DATABASE_POOL_SIZE", "20"))
    DATABASE_MAX_OVERFLOW: int = int(os.getenv("DATABASE_MAX_OVERFLOW", "30"))
    DATABASE_POOL_TIMEOUT: int = int(os.getenv("DATABASE_POOL_TIMEOUT", "30"))
    DATABASE_POOL_RECYCLE: int = int(os.getenv("DATABASE_POOL_RECYCLE", "3600"))
    DATABASE_ECHO: bool = os.getenv("DATABASE_ECHO", "False").lower() == "true"
    
    # API Keys (if using external services)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    HUGGINGFACE_API_KEY: str = os.getenv("HUGGINGFACE_API_KEY", "")
    
    # Phase 2 Enhancement Settings
    # Redis cache settings
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")
    
    # Celery settings
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    
    # Advanced processing settings
    ENABLE_ADVANCED_PDF: bool = os.getenv("ENABLE_ADVANCED_PDF", "True").lower() == "true"
    ENABLE_OBJECT_DETECTION: bool = os.getenv("ENABLE_OBJECT_DETECTION", "True").lower() == "true"
    ENABLE_HYBRID_SEARCH: bool = os.getenv("ENABLE_HYBRID_SEARCH", "True").lower() == "true"
    
    # Performance settings
    SEARCH_CACHE_TTL: int = int(os.getenv("SEARCH_CACHE_TTL", "3600"))  # 1 hour
    MAX_CONCURRENT_PROCESSES: int = int(os.getenv("MAX_CONCURRENT_PROCESSES", "4"))
    
    # Advanced PDF processing settings
    PDF_TABLE_EXTRACTION: bool = os.getenv("PDF_TABLE_EXTRACTION", "True").lower() == "true"
    PDF_IMAGE_EXTRACTION: bool = os.getenv("PDF_IMAGE_EXTRACTION", "True").lower() == "true"
    
    # Object detection model settings
    OBJECT_DETECTION_MODEL: str = os.getenv("OBJECT_DETECTION_MODEL", "yolov5s")
    OCR_CONFIDENCE_THRESHOLD: float = float(os.getenv("OCR_CONFIDENCE_THRESHOLD", "0.5"))
    
    def __init__(self):
        """Initialize settings and create directories"""
        self.create_directories()
    
    def create_directories(self):
        """Create necessary directories"""
        Path(self.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
        Path(self.INDEX_DIR).mkdir(parents=True, exist_ok=True)
    
    def is_allowed_file(self, filename: str) -> bool:
        """Check if file extension is allowed"""
        return any(filename.lower().endswith(ext) for ext in self.ALLOWED_EXTENSIONS)
