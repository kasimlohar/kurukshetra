"""
Database models for ConfluxAI with PostgreSQL support
"""

from sqlalchemy import Column, String, Text, DateTime, Float, JSON, ForeignKey, Boolean, Integer, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from datetime import datetime
import uuid

Base = declarative_base()

class Document(Base):
    """Document metadata and content storage"""
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    content = Column(Text)
    content_type = Column(String(100))
    file_size = Column(Float)
    file_hash = Column(String(64), unique=True, index=True)
    
    # Metadata stored as JSONB for better performance
    file_metadata = Column(JSONB)
    extracted_text = Column(Text)
    summary = Column(Text)
    keywords = Column(ARRAY(String))
    
    # Embeddings - store as JSONB for vector data
    embedding_vector = Column(JSONB)  # Array of floats
    embedding_model = Column(String(100))
    embedding_dimensions = Column(Integer)
    
    # Processing status
    processing_status = Column(String(50), default="pending", index=True)
    processing_error = Column(Text)
    processing_attempts = Column(Integer, default=0)
    
    # Search optimization
    search_vector = Column(Text)  # For full-text search
    language = Column(String(10), default="en")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    processed_at = Column(DateTime)
    indexed_at = Column(DateTime)
    
    # Relationships
    search_results = relationship("SearchResult", back_populates="document", cascade="all, delete-orphan")
    ai_interactions = relationship("AIInteraction", back_populates="document", cascade="all, delete-orphan")

    # Indexes for performance
    __table_args__ = (
        Index('idx_document_status_created', 'processing_status', 'created_at'),
        Index('idx_document_hash', 'file_hash'),
        Index('idx_document_content_type', 'content_type'),
    )

class SearchHistory(Base):
    """Search query history and analytics"""
    __tablename__ = "search_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query = Column(String(1000), nullable=False, index=True)
    query_hash = Column(String(64), index=True)  # For duplicate detection
    search_type = Column(String(50), index=True)  # semantic, keyword, hybrid
    filters = Column(JSONB)
    
    # Results and performance
    total_results = Column(Integer, default=0)
    processing_time = Column(Float)
    cache_hit = Column(Boolean, default=False)
    
    # User context
    user_id = Column(String(100), index=True)
    session_id = Column(String(100), index=True)
    ip_address = Column(String(45))  # IPv6 compatible
    user_agent = Column(Text)
    
    # Query analysis
    query_intent = Column(String(100))
    query_complexity = Column(String(50))
    query_language = Column(String(10))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    search_results = relationship("SearchResult", back_populates="search_query", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index('idx_search_user_time', 'user_id', 'created_at'),
        Index('idx_search_type_time', 'search_type', 'created_at'),
        Index('idx_search_query_hash', 'query_hash'),
    )

class SearchResult(Base):
    """Individual search result entries"""
    __tablename__ = "search_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    search_id = Column(UUID(as_uuid=True), ForeignKey("search_history.id", ondelete="CASCADE"), nullable=False)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    
    # Relevance metrics
    similarity_score = Column(Float, index=True)
    rank_position = Column(Integer)
    relevance_factors = Column(JSONB)  # Store detailed scoring factors
    
    # User interaction
    clicked = Column(Boolean, default=False)
    view_duration = Column(Float)  # Time spent viewing in seconds
    user_rating = Column(Integer)  # 1-5 rating
    user_feedback = Column(Text)
    
    # Context at time of search
    result_snippet = Column(Text)
    highlighted_terms = Column(ARRAY(String))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    clicked_at = Column(DateTime)
    rated_at = Column(DateTime)
    
    # Relationships
    search_query = relationship("SearchHistory", back_populates="search_results")
    document = relationship("Document", back_populates="search_results")

    # Indexes
    __table_args__ = (
        Index('idx_result_search_rank', 'search_id', 'rank_position'),
        Index('idx_result_similarity', 'similarity_score'),
        Index('idx_result_clicked', 'clicked', 'created_at'),
    )

class AIInteraction(Base):
    """AI service usage tracking"""
    __tablename__ = "ai_interactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="SET NULL"), nullable=True)
    
    # Interaction details
    service_type = Column(String(50), nullable=False, index=True)  # summarization, qa, analysis, chat
    input_text = Column(Text)
    output_text = Column(Text)
    context = Column(JSONB)  # Additional context data
    
    # Model information
    model_name = Column(String(100))
    model_version = Column(String(50))
    model_provider = Column(String(50))  # openai, huggingface, local
    
    # Performance metrics
    processing_time = Column(Float)
    input_tokens = Column(Integer)
    output_tokens = Column(Integer)
    total_tokens = Column(Integer)
    cost = Column(Float)  # API cost if applicable
    
    # Quality metrics
    confidence_score = Column(Float)
    user_rating = Column(Integer)  # 1-5 rating
    user_feedback = Column(Text)
    error_message = Column(Text)
    
    # Request metadata
    request_id = Column(String(100), index=True)
    user_id = Column(String(100), index=True)
    session_id = Column(String(100), index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    completed_at = Column(DateTime)
    
    # Relationships
    document = relationship("Document", back_populates="ai_interactions")

    # Indexes
    __table_args__ = (
        Index('idx_ai_service_time', 'service_type', 'created_at'),
        Index('idx_ai_user_time', 'user_id', 'created_at'),
        Index('idx_ai_model', 'model_name', 'model_provider'),
    )

class SystemMetrics(Base):
    """System performance and health metrics"""
    __tablename__ = "system_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    metric_name = Column(String(100), nullable=False, index=True)
    metric_value = Column(Float)
    metric_unit = Column(String(20))
    metric_tags = Column(JSONB)  # Additional metadata tags
    
    # Context
    service_name = Column(String(100), index=True)
    instance_id = Column(String(100))
    environment = Column(String(50))  # dev, staging, prod
    
    # Aggregation support
    aggregation_period = Column(String(20))  # minute, hour, day
    sample_count = Column(Integer)
    
    # Timestamps
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Indexes
    __table_args__ = (
        Index('idx_metrics_service_time', 'service_name', 'timestamp'),
        Index('idx_metrics_name_time', 'metric_name', 'timestamp'),
    )

class UserSession(Base):
    """User session tracking"""
    __tablename__ = "user_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_token = Column(String(255), unique=True, index=True)
    user_id = Column(String(100), index=True)
    
    # Session details
    ip_address = Column(String(45))
    user_agent = Column(Text)
    device_type = Column(String(50))
    browser = Column(String(100))
    os = Column(String(100))
    
    # Geolocation
    country = Column(String(2))
    region = Column(String(100))
    city = Column(String(100))
    
    # Activity tracking
    pages_visited = Column(JSONB, default=list)
    actions_performed = Column(JSONB, default=list)
    search_count = Column(Integer, default=0)
    document_views = Column(Integer, default=0)
    
    # Session state
    preferences = Column(JSONB, default=dict)
    last_query = Column(String(1000))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow, index=True)
    expires_at = Column(DateTime, index=True)
    ended_at = Column(DateTime)
    is_active = Column(Boolean, default=True, index=True)
    
    # Performance
    session_duration = Column(Float)  # Calculated on session end
    
    # Indexes
    __table_args__ = (
        Index('idx_session_user_active', 'user_id', 'is_active'),
        Index('idx_session_token', 'session_token'),
        Index('idx_session_expires', 'expires_at'),
    )

class KnowledgeGraph(Base):
    """Knowledge graph entities and relationships"""
    __tablename__ = "knowledge_graph"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_name = Column(String(200), nullable=False, index=True)
    entity_type = Column(String(50), index=True)  # person, organization, concept, etc.
    entity_description = Column(Text)
    
    # Connections
    related_entities = Column(JSONB)  # List of related entity IDs
    relationship_types = Column(JSONB)  # Types of relationships
    
    # Document associations
    source_documents = Column(ARRAY(UUID))  # Document IDs where entity appears
    mention_count = Column(Integer, default=1)
    confidence_score = Column(Float)
    
    # Metadata
    aliases = Column(ARRAY(String))  # Alternative names
    attributes = Column(JSONB)  # Additional properties
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Indexes
    __table_args__ = (
        Index('idx_kg_entity_type', 'entity_type', 'entity_name'),
        Index('idx_kg_mention_count', 'mention_count'),
    )

class TaskQueue(Base):
    """Async task queue for background processing"""
    __tablename__ = "task_queue"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_type = Column(String(50), nullable=False, index=True)
    task_name = Column(String(100))
    task_data = Column(JSONB)  # Task parameters
    
    # Status tracking
    status = Column(String(20), default="pending", index=True)  # pending, processing, completed, failed
    priority = Column(Integer, default=5, index=True)  # 1-10, higher = more priority
    max_retries = Column(Integer, default=3)
    retry_count = Column(Integer, default=0)
    
    # Processing info
    worker_id = Column(String(100))
    error_message = Column(Text)
    result_data = Column(JSONB)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    next_retry_at = Column(DateTime)
    
    # Indexes
    __table_args__ = (
        Index('idx_task_status_priority', 'status', 'priority', 'created_at'),
        Index('idx_task_type_status', 'task_type', 'status'),
        Index('idx_task_retry', 'next_retry_at'),
    )
