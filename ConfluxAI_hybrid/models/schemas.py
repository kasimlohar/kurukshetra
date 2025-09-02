"""
Pydantic models for ConfluxAI Multi-Modal Search Agent
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union, Tuple
from datetime import datetime
from enum import Enum

# Phase 2 Enhanced Models

class TaskStatus(str, Enum):
    """Task status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
    NOT_FOUND = "not_found"
    UNKNOWN = "unknown"

class TaskResponse(BaseModel):
    """Background task response model"""
    task_id: str = Field(..., description="Unique task identifier")
    status: Union[TaskStatus, str] = Field(..., description="Current task status")
    message: str = Field(..., description="Task status message")
    submitted_at: datetime = Field(..., description="Task submission time")
    started_at: Optional[datetime] = Field(None, description="Task start time")
    completed_at: Optional[datetime] = Field(None, description="Task completion time")
    progress: float = Field(default=0.0, description="Task progress percentage (0-100)")
    result: Optional[Dict[str, Any]] = Field(None, description="Task result data")
    error: Optional[str] = Field(None, description="Error message if failed")
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")
    metadata: Dict[str, Any] = Field(default={}, description="Additional task metadata")

class BatchProcessingRequest(BaseModel):
    """Batch file processing request"""
    files: List[Dict[str, Any]] = Field(..., description="List of files to process")
    priority: int = Field(default=5, description="Processing priority (1-10)")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Batch metadata")
    async_processing: bool = Field(default=True, description="Enable async processing")

class CacheStats(BaseModel):
    """Cache service statistics"""
    status: str = Field(..., description="Cache service status")
    redis_info: Optional[Dict[str, Any]] = Field(default=None, description="Redis server information")
    cache_keys: Dict[str, int] = Field(default={}, description="Cache key counts by type")
    total_keys: int = Field(default=0, description="Total cache keys")
    hit_rate: Optional[float] = Field(default=None, description="Cache hit rate")
    memory_usage: Optional[str] = Field(default=None, description="Memory usage")

class SearchAnalytics(BaseModel):
    """Search analytics and performance metrics"""
    query: str = Field(..., description="Search query")
    result_count: int = Field(..., description="Number of results returned")
    processing_time: float = Field(..., description="Search processing time")
    search_type: str = Field(..., description="Type of search performed")
    cache_hit: bool = Field(default=False, description="Whether result was cached")
    user_agent: Optional[str] = Field(None, description="User agent string")
    timestamp: datetime = Field(default_factory=datetime.now, description="Search timestamp")

class AdvancedSearchFilters(BaseModel):
    """Advanced search filtering options"""
    file_types: Optional[List[str]] = Field(None, description="Filter by file extensions")
    content_types: Optional[List[str]] = Field(None, description="Filter by MIME types")
    date_from: Optional[datetime] = Field(None, description="Filter from date")
    date_to: Optional[datetime] = Field(None, description="Filter to date")
    file_size_min: Optional[int] = Field(None, description="Minimum file size in bytes")
    file_size_max: Optional[int] = Field(None, description="Maximum file size in bytes")
    authors: Optional[List[str]] = Field(None, description="Filter by document authors")
    tags: Optional[List[str]] = Field(None, description="Filter by tags")
    metadata_filters: Optional[Dict[str, Any]] = Field(None, description="Custom metadata filters")
    exclude_files: Optional[List[str]] = Field(None, description="File IDs to exclude")

class SearchExplanation(BaseModel):
    """Search result explanation"""
    query: str = Field(..., description="Original search query")
    result_id: str = Field(..., description="Result identifier")
    total_score: float = Field(..., description="Total relevance score")
    semantic_score: Optional[float] = Field(None, description="Semantic similarity score")
    keyword_score: Optional[float] = Field(None, description="Keyword matching score")
    matching_terms: List[str] = Field(default=[], description="Matching query terms")
    match_ratio: float = Field(..., description="Ratio of matching terms")
    boost_factors: Optional[Dict[str, float]] = Field(default=None, description="Score boost factors")

class SystemHealth(BaseModel):
    """Overall system health status"""
    status: str = Field(..., description="Overall system status")
    services: Dict[str, Dict[str, Any]] = Field(..., description="Individual service health")
    uptime: float = Field(..., description="System uptime in seconds")
    memory_usage: Optional[Dict[str, Any]] = Field(None, description="Memory usage statistics")
    disk_usage: Optional[Dict[str, Any]] = Field(None, description="Disk usage statistics")
    performance_metrics: Optional[Dict[str, Any]] = Field(None, description="Performance metrics")
    timestamp: datetime = Field(default_factory=datetime.now, description="Health check timestamp")

class FileProcessingConfig(BaseModel):
    """File processing configuration"""
    enable_advanced_pdf: bool = Field(default=True, description="Enable advanced PDF processing")
    enable_object_detection: bool = Field(default=True, description="Enable image object detection")
    enable_table_extraction: bool = Field(default=True, description="Enable table extraction")
    ocr_confidence_threshold: float = Field(default=0.5, description="OCR confidence threshold")
    max_file_size_mb: int = Field(default=50, description="Maximum file size in MB")

# Phase 3 AI Feature Models

class SummaryRequest(BaseModel):
    """Document summarization request"""
    text: Optional[str] = Field(None, description="Text to summarize")
    document_id: Optional[str] = Field(None, description="Document ID to summarize")
    max_length: int = Field(default=150, description="Maximum summary length")
    summary_type: str = Field(default="standard", description="Type of summary: standard, bullet_points, sections")

class SummaryResponse(BaseModel):
    """Document summarization response"""
    summary: str = Field(..., description="Generated summary")
    key_points: List[str] = Field(default=[], description="Key points extracted")
    confidence: float = Field(..., description="Summary quality confidence")
    original_length: int = Field(..., description="Original text length in words")
    summary_length: int = Field(..., description="Summary length in words")
    compression_ratio: float = Field(..., description="Compression ratio")
    processing_time: float = Field(..., description="Processing time in seconds")

class QuestionRequest(BaseModel):
    """Question answering request"""
    question: str = Field(..., description="Question to answer")
    context_limit: int = Field(default=5, description="Maximum number of documents to consider")
    file_filters: Optional[List[str]] = Field(None, description="Filter by file types")
    confidence_threshold: float = Field(default=0.3, description="Minimum confidence for answers")

class QuestionResponse(BaseModel):
    """Question answering response"""
    question: str = Field(..., description="Original question")
    answer: str = Field(..., description="Generated answer")
    confidence: float = Field(..., description="Answer confidence score")
    sources: List[Dict[str, Any]] = Field(default=[], description="Source documents")
    context_used: str = Field(..., description="Context used for answering")
    follow_up_questions: List[str] = Field(default=[], description="Suggested follow-up questions")
    processing_time: float = Field(..., description="Processing time in seconds")

class ContentAnalysisRequest(BaseModel):
    """Content analysis request"""
    text: Optional[str] = Field(None, description="Text to analyze")
    document_id: Optional[str] = Field(None, description="Document ID to analyze")
    analysis_types: List[str] = Field(
        default=["classification", "entities", "sentiment", "topics"],
        description="Types of analysis to perform"
    )

class ContentAnalysisResponse(BaseModel):
    """Content analysis response"""
    document_type: str = Field(..., description="Classified document type")
    confidence: float = Field(..., description="Classification confidence")
    topics: List[Tuple[str, float]] = Field(default=[], description="Extracted topics with relevance scores")
    sentiment: Dict[str, float] = Field(..., description="Sentiment analysis scores")
    language: str = Field(..., description="Detected language")
    complexity_score: float = Field(..., description="Text complexity score")
    entities: List[Dict[str, Any]] = Field(default=[], description="Extracted entities")
    entity_counts: Dict[str, int] = Field(default={}, description="Entity type counts")
    relationships: List[Dict[str, Any]] = Field(default=[], description="Entity relationships")
    processing_time: float = Field(..., description="Processing time in seconds")

class MultiDocumentQARequest(BaseModel):
    """Multi-document question answering request"""
    question: str = Field(..., description="Question to answer")
    file_filters: Optional[List[str]] = Field(None, description="Filter by file types")
    max_documents: int = Field(default=6, description="Maximum documents to analyze")
    aggregation_method: str = Field(default="consensus", description="Answer aggregation method")

class MultiDocumentQAResponse(BaseModel):
    """Multi-document question answering response"""
    question: str = Field(..., description="Original question")
    aggregated_answer: str = Field(..., description="Aggregated answer from multiple sources")
    individual_answers: List[Dict[str, Any]] = Field(default=[], description="Individual answers from each document")
    confidence: float = Field(..., description="Overall confidence score")
    source_count: int = Field(..., description="Number of sources used")
    consensus_level: str = Field(..., description="Level of consensus between sources")
    processing_time: float = Field(..., description="Processing time in seconds")

class AIServiceStatus(BaseModel):
    """AI service status response"""
    service_name: str = Field(..., description="Name of the AI service")
    initialized: bool = Field(..., description="Whether service is initialized")
    models_loaded: Dict[str, bool] = Field(..., description="Status of loaded models")
    capabilities: Dict[str, bool] = Field(..., description="Available capabilities")
    performance_metrics: Optional[Dict[str, Any]] = Field(None, description="Performance statistics")
    device_info: str = Field(..., description="Device information (CPU/GPU)")
    memory_usage: Optional[str] = Field(None, description="Memory usage information")

class SearchSuggestion(BaseModel):
    """Search suggestion response"""
    suggestions: List[str] = Field(..., description="List of search suggestions")
    query_completions: List[str] = Field(default=[], description="Query auto-completions")
    related_topics: List[str] = Field(default=[], description="Related topic suggestions")
    popular_queries: List[str] = Field(default=[], description="Popular recent queries")

# WebSocket Message Models for Real-time Features

class WebSocketMessage(BaseModel):
    """Base WebSocket message"""
    type: str = Field(..., description="Message type")
    timestamp: datetime = Field(default_factory=datetime.now, description="Message timestamp")
    data: Dict[str, Any] = Field(..., description="Message data")

class SearchProgressUpdate(BaseModel):
    """Real-time search progress update"""
    search_id: str = Field(..., description="Search session ID")
    stage: str = Field(..., description="Current processing stage")
    progress: float = Field(..., description="Progress percentage (0-100)")
    message: str = Field(..., description="Progress message")
    partial_results: Optional[List["SearchResult"]] = Field(None, description="Partial search results")

class ProcessingProgressUpdate(BaseModel):
    """Real-time file processing progress update"""
    task_id: str = Field(..., description="Processing task ID")
    filename: str = Field(..., description="File being processed")
    stage: str = Field(..., description="Current processing stage")
    progress: float = Field(..., description="Progress percentage (0-100)")
    estimated_time_remaining: Optional[float] = Field(None, description="Estimated time remaining in seconds")

class SystemNotification(BaseModel):
    """System notification message"""
    level: str = Field(..., description="Notification level: info, warning, error")
    title: str = Field(..., description="Notification title")
    message: str = Field(..., description="Notification message")
    action_required: bool = Field(default=False, description="Whether user action is required")
    action_url: Optional[str] = Field(None, description="URL for action if required")
    chunk_size: int = Field(default=512, description="Text chunk size")
    chunk_overlap: int = Field(default=50, description="Chunk overlap size")

class PerformanceMetrics(BaseModel):
    """System performance metrics"""
    search_response_time_avg: float = Field(..., description="Average search response time (ms)")
    file_processing_time_avg: float = Field(..., description="Average file processing time (ms)")
    indexing_throughput: float = Field(..., description="Files indexed per hour")
    cache_hit_rate: float = Field(..., description="Cache hit rate percentage")
    active_connections: int = Field(..., description="Number of active connections")
    memory_usage_percent: float = Field(..., description="Memory usage percentage")
    cpu_usage_percent: float = Field(..., description="CPU usage percentage")
    disk_usage_percent: float = Field(..., description="Disk usage percentage")

class SearchResult(BaseModel):
    """Individual search result"""
    content: str = Field(..., description="Content of the search result")
    score: float = Field(..., description="Similarity score")
    file_id: Optional[str] = Field(None, description="Source file identifier")
    filename: Optional[str] = Field(None, description="Source filename")
    chunk_id: Optional[str] = Field(None, description="Chunk identifier")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    content_type: str = Field(..., description="Type of content (text, image, etc.)")

class SearchRequest(BaseModel):
    """Search request model"""
    query: str = Field(..., description="Search query string")
    limit: int = Field(default=10, description="Maximum number of results")
    threshold: float = Field(default=0.7, description="Similarity threshold")
    filters: Optional[Dict[str, Any]] = Field(None, description="Search filters")

class SearchResponse(BaseModel):
    """Search response model"""
    query: str = Field(..., description="Original search query")
    results: List[SearchResult] = Field(..., description="Search results")
    total_results: int = Field(..., description="Total number of results")
    processing_time: float = Field(..., description="Processing time in seconds")
    suggestions: Optional[List[str]] = Field(None, description="Query suggestions")

class IndexedFile(BaseModel):
    """Indexed file information"""
    filename: str = Field(..., description="Name of the indexed file")
    file_id: str = Field(..., description="Unique file identifier")
    chunks_indexed: int = Field(..., description="Number of chunks created")

class FailedFile(BaseModel):
    """Failed file indexing information"""
    filename: str = Field(..., description="Name of the failed file")
    error: str = Field(..., description="Error message")

class IndexResponse(BaseModel):
    """Index response model"""
    success: bool = Field(..., description="Whether indexing was successful")
    indexed_files: List[IndexedFile] = Field(..., description="Successfully indexed files")
    failed_files: List[FailedFile] = Field(..., description="Failed file indexing")
    total_indexed: int = Field(..., description="Total number of indexed files")
    message: str = Field(..., description="Response message")

class ServiceStatus(BaseModel):
    """Service status model"""
    status: str = Field(..., description="Service status")
    last_check: datetime = Field(..., description="Last health check time")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional status details")

class HealthResponse(BaseModel):
    """Health check response model"""
    status: str = Field(..., description="Overall system status")
    timestamp: datetime = Field(..., description="Health check timestamp")
    services: Dict[str, ServiceStatus] = Field(..., description="Individual service statuses")

class FileMetadata(BaseModel):
    """File metadata model"""
    file_id: str = Field(..., description="Unique file identifier")
    filename: str = Field(..., description="Original filename")
    file_type: str = Field(..., description="File type/extension")
    file_size: int = Field(..., description="File size in bytes")
    upload_time: datetime = Field(..., description="Upload timestamp")
    content_type: str = Field(..., description="MIME content type")
    processed: bool = Field(..., description="Whether file has been processed")
    chunks_count: int = Field(default=0, description="Number of chunks created")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

class IndexStats(BaseModel):
    """Index statistics model"""
    total_files: int = Field(..., description="Total number of indexed files")
    total_chunks: int = Field(..., description="Total number of chunks")
    index_size: float = Field(..., description="Index size in MB")
    last_updated: datetime = Field(..., description="Last update timestamp")
    file_types: Dict[str, int] = Field(..., description="Count by file type")

class ChunkData(BaseModel):
    """Text chunk data model"""
    chunk_id: str = Field(..., description="Unique chunk identifier")
    content: str = Field(..., description="Chunk content")
    file_id: str = Field(..., description="Source file identifier")
    chunk_index: int = Field(..., description="Chunk position in file")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Chunk metadata")

class ImageAnalysis(BaseModel):
    """Image analysis result model"""
    description: str = Field(..., description="Image description")
    objects: List[str] = Field(..., description="Detected objects")
    text_content: Optional[str] = Field(None, description="Extracted text from image")
    features: Optional[Dict[str, Any]] = Field(None, description="Image features")
    confidence_scores: Optional[Dict[str, float]] = Field(None, description="Confidence scores")
    bounding_boxes: Optional[List[Dict[str, Any]]] = Field(None, description="Object bounding boxes")
    ocr_confidence: Optional[float] = Field(None, description="OCR confidence score")

class TableData(BaseModel):
    """Table extraction result model"""
    table_id: str = Field(..., description="Unique table identifier")
    headers: List[str] = Field(..., description="Table headers")
    rows: List[List[str]] = Field(..., description="Table rows")
    confidence: float = Field(..., description="Extraction confidence")
    page_number: Optional[int] = Field(None, description="Page number where table was found")
    position: Optional[Dict[str, float]] = Field(None, description="Table position on page")

class PDFAnalysis(BaseModel):
    """Enhanced PDF analysis result model"""
    text_content: str = Field(..., description="Extracted text content")
    tables: List[TableData] = Field(default=[], description="Extracted tables")
    images: List[ImageAnalysis] = Field(default=[], description="Extracted images")
    metadata: Dict[str, Any] = Field(default={}, description="PDF metadata")
    page_count: int = Field(..., description="Number of pages")
    layout_preserved: bool = Field(default=False, description="Whether layout was preserved")

class ProcessingResult(BaseModel):
    """File processing result model"""
    file_id: str = Field(..., description="File identifier")
    content_type: str = Field(..., description="Detected content type")
    text_content: Optional[str] = Field(None, description="Extracted text content")
    image_analysis: Optional[ImageAnalysis] = Field(None, description="Image analysis results")
    pdf_analysis: Optional[PDFAnalysis] = Field(None, description="Enhanced PDF analysis results")
    chunks: List[ChunkData] = Field(..., description="Generated chunks")
    metadata: Dict[str, Any] = Field(..., description="Processing metadata")
    processing_time: float = Field(..., description="Processing time in seconds")

class HybridSearchRequest(BaseModel):
    """Hybrid search request model"""
    query: str = Field(..., description="Search query string")
    limit: int = Field(default=10, description="Maximum number of results")
    threshold: float = Field(default=0.7, description="Similarity threshold")
    semantic_weight: float = Field(default=0.7, description="Weight for semantic search (0-1)")
    keyword_weight: float = Field(default=0.3, description="Weight for keyword search (0-1)")
    file_types: List[str] = Field(default=[], description="Filter by file types")
    date_from: Optional[datetime] = Field(default=None, description="Filter from date")
    date_to: Optional[datetime] = Field(default=None, description="Filter to date")
    content_types: List[str] = Field(default=[], description="Filter by content types")
    metadata_filters: Optional[Dict[str, Any]] = Field(default=None, description="Metadata filters")
    sort_by: str = Field(default="relevance", description="Sort order")
    facets: bool = Field(default=False, description="Include faceted results")

class SearchFacets(BaseModel):
    """Search facets model"""
    file_types: Dict[str, int] = Field(default={}, description="Count by file type")
    content_types: Dict[str, int] = Field(default={}, description="Count by content type")
    date_ranges: Dict[str, int] = Field(default={}, description="Count by date range")
    authors: Dict[str, int] = Field(default={}, description="Count by author")

class EnhancedSearchResponse(BaseModel):
    """Enhanced search response model"""
    query: str = Field(..., description="Original search query")
    results: List[SearchResult] = Field(..., description="Search results")
    total_results: int = Field(..., description="Total number of results")
    processing_time: float = Field(..., description="Processing time in seconds")
    suggestions: Optional[List[str]] = Field(default=None, description="Query suggestions")
    facets: Optional[SearchFacets] = Field(default=None, description="Search facets")
    search_type: str = Field(default="hybrid", description="Type of search performed")

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")
