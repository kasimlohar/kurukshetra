"""
Indexing service for ConfluxAI Multi-Modal Search Agent
Handles file indexing and metadata management
"""
import os
import json
import sqlite3
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import asyncio

from models.schemas import ServiceStatus, ProcessingResult, IndexStats, FileMetadata
from config.settings import Settings
from utils.file_processor import FileProcessor
from services.search_service import SearchService

logger = logging.getLogger(__name__)

class IndexingService:
    """Handles file indexing operations"""
    
    def __init__(self):
        self.settings = Settings()
        self.file_processor = FileProcessor()
        self.search_service = None  # Will be injected
        self.db_path = os.path.join(self.settings.INDEX_DIR, "metadata.db")
        self.initialized = False
    
    async def initialize(self):
        """Initialize the indexing service"""
        try:
            logger.info("Initializing indexing service...")
            
            # Create database tables
            await self._create_tables()
            
            self.initialized = True
            logger.info("Indexing service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize indexing service: {str(e)}")
            raise
    
    def set_search_service(self, search_service: SearchService):
        """Set the search service reference"""
        self.search_service = search_service
    
    async def _create_tables(self):
        """Create database tables for metadata"""
        try:
            # Ensure directory exists
            os.makedirs(self.settings.INDEX_DIR, exist_ok=True)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Files table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS files (
                    file_id TEXT PRIMARY KEY,
                    filename TEXT NOT NULL,
                    file_type TEXT NOT NULL,
                    file_size INTEGER NOT NULL,
                    content_type TEXT NOT NULL,
                    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    processed BOOLEAN DEFAULT FALSE,
                    chunks_count INTEGER DEFAULT 0,
                    metadata TEXT
                )
            """)
            
            # Chunks table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chunks (
                    chunk_id TEXT PRIMARY KEY,
                    file_id TEXT NOT NULL,
                    chunk_index INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    chunk_metadata TEXT,
                    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (file_id) REFERENCES files (file_id)
                )
            """)
            
            # Create indexes
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_file_id ON chunks (file_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_upload_time ON files (upload_time)")
            
            conn.commit()
            conn.close()
            
            logger.info("Database tables created successfully")
            
        except Exception as e:
            logger.error(f"Error creating database tables: {str(e)}")
            raise
    
    async def index_file(
        self, 
        file_path: str, 
        filename: str, 
        metadata: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Index a file and add it to the search database
        
        Args:
            file_path: Path to the file
            filename: Original filename
            metadata: Optional metadata as JSON string
            
        Returns:
            Dictionary with indexing results
        """
        try:
            if not self.initialized:
                raise Exception("Indexing service not initialized")
            
            logger.info(f"Indexing file: {filename}")
            
            # Check if file type is allowed
            if not self.settings.is_allowed_file(filename):
                raise Exception(f"File type not allowed: {filename}")
            
            # Process the file
            processing_result = await self.file_processor.process_file(file_path, filename)
            
            # Store metadata in database
            await self._store_file_metadata(processing_result, metadata)
            
            # Add to search index if search service is available
            if self.search_service and self.search_service.initialized:
                await self.search_service.add_documents(processing_result)
            
            logger.info(f"Successfully indexed file {filename} with {len(processing_result.chunks)} chunks")
            
            return {
                'file_id': processing_result.file_id,
                'chunks_indexed': len(processing_result.chunks),
                'processing_time': processing_result.processing_time
            }
            
        except Exception as e:
            logger.error(f"Error indexing file {filename}: {str(e)}")
            raise
    
    async def _store_file_metadata(self, processing_result: ProcessingResult, metadata: Optional[str] = None):
        """Store file and chunk metadata in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Store file metadata
            cursor.execute("""
                INSERT INTO files (
                    file_id, filename, file_type, file_size, content_type,
                    processed, chunks_count, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                processing_result.file_id,
                processing_result.metadata.get('filename', ''),
                processing_result.content_type.split('/')[-1] if '/' in processing_result.content_type else processing_result.content_type,
                processing_result.metadata.get('file_size', 0),
                processing_result.content_type,
                True,
                len(processing_result.chunks),
                json.dumps({
                    'original_metadata': json.loads(metadata) if metadata else {},
                    'processing_metadata': processing_result.metadata
                })
            ))
            
            # Store chunk metadata
            for chunk in processing_result.chunks:
                cursor.execute("""
                    INSERT INTO chunks (
                        chunk_id, file_id, chunk_index, content, chunk_metadata
                    ) VALUES (?, ?, ?, ?, ?)
                """, (
                    chunk.chunk_id,
                    processing_result.file_id,
                    chunk.chunk_index,
                    chunk.content,
                    json.dumps(chunk.metadata) if chunk.metadata else None
                ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error storing metadata: {str(e)}")
            raise
    
    async def delete_file(self, file_id: str) -> bool:
        """Delete a file and its chunks from the index"""
        try:
            if not self.initialized:
                raise Exception("Indexing service not initialized")
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if file exists
            cursor.execute("SELECT COUNT(*) FROM files WHERE file_id = ?", (file_id,))
            if cursor.fetchone()[0] == 0:
                conn.close()
                return False
            
            # Delete from search index if available
            if self.search_service and self.search_service.initialized:
                await self.search_service.delete_file_documents(file_id)
            
            # Delete chunks
            cursor.execute("DELETE FROM chunks WHERE file_id = ?", (file_id,))
            
            # Delete file record
            cursor.execute("DELETE FROM files WHERE file_id = ?", (file_id,))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Deleted file {file_id} from index")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting file {file_id}: {str(e)}")
            raise
    
    async def get_file_metadata(self, file_id: str) -> Optional[FileMetadata]:
        """Get metadata for a specific file"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT file_id, filename, file_type, file_size, content_type,
                       upload_time, processed, chunks_count, metadata
                FROM files WHERE file_id = ?
            """, (file_id,))
            
            row = cursor.fetchone()
            conn.close()
            
            if not row:
                return None
            
            return FileMetadata(
                file_id=row[0],
                filename=row[1],
                file_type=row[2],
                file_size=row[3],
                content_type=row[4],
                upload_time=datetime.fromisoformat(row[5]),
                processed=bool(row[6]),
                chunks_count=row[7],
                metadata=json.loads(row[8]) if row[8] else None
            )
            
        except Exception as e:
            logger.error(f"Error getting file metadata: {str(e)}")
            return None
    
    async def list_files(self, limit: int = 100, offset: int = 0) -> List[FileMetadata]:
        """List indexed files"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT file_id, filename, file_type, file_size, content_type,
                       upload_time, processed, chunks_count, metadata
                FROM files
                ORDER BY upload_time DESC
                LIMIT ? OFFSET ?
            """, (limit, offset))
            
            rows = cursor.fetchall()
            conn.close()
            
            files = []
            for row in rows:
                files.append(FileMetadata(
                    file_id=row[0],
                    filename=row[1],
                    file_type=row[2],
                    file_size=row[3],
                    content_type=row[4],
                    upload_time=datetime.fromisoformat(row[5]),
                    processed=bool(row[6]),
                    chunks_count=row[7],
                    metadata=json.loads(row[8]) if row[8] else None
                ))
            
            return files
            
        except Exception as e:
            logger.error(f"Error listing files: {str(e)}")
            return []
    
    async def get_stats(self) -> IndexStats:
        """Get indexing statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total files and chunks
            cursor.execute("SELECT COUNT(*) FROM files")
            total_files = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM chunks")
            total_chunks = cursor.fetchone()[0]
            
            # File types
            cursor.execute("SELECT file_type, COUNT(*) FROM files GROUP BY file_type")
            file_types = dict(cursor.fetchall())
            
            # Last updated
            cursor.execute("SELECT MAX(upload_time) FROM files")
            last_updated_str = cursor.fetchone()[0]
            last_updated = datetime.fromisoformat(last_updated_str) if last_updated_str else datetime.utcnow()
            
            conn.close()
            
            # Calculate index size (approximate)
            index_size = 0.0
            if os.path.exists(self.db_path):
                index_size = os.path.getsize(self.db_path) / (1024 * 1024)  # MB
            
            return IndexStats(
                total_files=total_files,
                total_chunks=total_chunks,
                index_size=index_size,
                last_updated=last_updated,
                file_types=file_types
            )
            
        except Exception as e:
            logger.error(f"Error getting stats: {str(e)}")
            return IndexStats(
                total_files=0,
                total_chunks=0,
                index_size=0.0,
                last_updated=datetime.utcnow(),
                file_types={}
            )
    
    async def health_check(self) -> ServiceStatus:
        """Check service health"""
        try:
            # Test database connection
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM files")
            file_count = cursor.fetchone()[0]
            conn.close()
            
            status = "healthy" if self.initialized else "unhealthy"
            
            details = {
                'initialized': self.initialized,
                'database_accessible': True,
                'indexed_files': file_count
            }
            
            return ServiceStatus(
                status=status,
                last_check=datetime.utcnow(),
                details=details
            )
            
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return ServiceStatus(
                status="unhealthy",
                last_check=datetime.utcnow(),
                details={'error': str(e)}
            )
    
    async def cleanup(self):
        """Cleanup resources"""
        try:
            # Close any open connections
            logger.info("Indexing service cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
    
    async def reindex_all(self):
        """Reindex all files (useful for schema updates)"""
        try:
            logger.info("Starting reindexing of all files...")
            
            # Get all files
            files = await self.list_files(limit=10000)
            
            for file_metadata in files:
                try:
                    # This would require storing original file paths
                    # For now, just log the operation
                    logger.info(f"Would reindex file: {file_metadata.filename}")
                except Exception as e:
                    logger.error(f"Error reindexing file {file_metadata.filename}: {str(e)}")
            
            logger.info("Reindexing completed")
            
        except Exception as e:
            logger.error(f"Error during reindexing: {str(e)}")
            raise
