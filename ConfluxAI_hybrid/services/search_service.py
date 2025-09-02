"""
Search service for ConfluxAI Multi-Modal Search Agent
Handles vector embeddings and similarity search using FAISS
"""
import os
import json
import pickle
import logging
from typing import List, Dict, Any, Optional
import asyncio
from datetime import datetime
import numpy as np

# Vector embeddings
try:
    from sentence_transformers import SentenceTransformer
    import faiss
except ImportError:
    SentenceTransformer = None
    faiss = None

from models.schemas import SearchResult, ServiceStatus, ProcessingResult
from config.settings import Settings

logger = logging.getLogger(__name__)

class SearchService:
    """Handles vector-based search operations"""
    
    def __init__(self):
        self.settings = Settings()
        self.encoder = None
        self.index = None
        self.documents = []  # Store document metadata
        self.initialized = False
        self.index_path = os.path.join(self.settings.INDEX_DIR, f"{self.settings.INDEX_NAME}.faiss")
        self.metadata_path = os.path.join(self.settings.INDEX_DIR, f"{self.settings.INDEX_NAME}_metadata.pkl")
    
    async def initialize(self):
        """Initialize the search service"""
        try:
            logger.info("Initializing search service...")
            
            if not SentenceTransformer or not faiss:
                raise Exception("Required libraries (sentence-transformers, faiss) not available")
            
            # Load embedding model
            logger.info(f"Loading embedding model: {self.settings.EMBEDDING_MODEL}")
            self.encoder = SentenceTransformer(self.settings.EMBEDDING_MODEL)
            
            # Load or create FAISS index
            await self._load_or_create_index()
            
            self.initialized = True
            logger.info("Search service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize search service: {str(e)}")
            raise
    
    async def _load_or_create_index(self):
        """Load existing index or create new one"""
        try:
            if os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
                # Load existing index
                logger.info("Loading existing search index...")
                self.index = faiss.read_index(self.index_path)
                
                with open(self.metadata_path, 'rb') as f:
                    self.documents = pickle.load(f)
                
                logger.info(f"Loaded index with {len(self.documents)} documents")
            else:
                # Create new index
                logger.info("Creating new search index...")
                self.index = faiss.IndexFlatIP(self.settings.VECTOR_DIM)  # Inner product (cosine similarity)
                self.documents = []
                
                # Save empty index
                await self._save_index()
                
        except Exception as e:
            logger.error(f"Error loading/creating index: {str(e)}")
            raise
    
    async def _save_index(self):
        """Save index and metadata to disk"""
        try:
            # Ensure directory exists
            os.makedirs(self.settings.INDEX_DIR, exist_ok=True)
            
            # Save FAISS index
            faiss.write_index(self.index, self.index_path)
            
            # Save metadata
            with open(self.metadata_path, 'wb') as f:
                pickle.dump(self.documents, f)
                
            logger.info("Index saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving index: {str(e)}")
            raise
    
    async def add_documents(self, processing_result: ProcessingResult):
        """Add documents to the search index"""
        try:
            if not self.initialized:
                raise Exception("Search service not initialized")
            
            vectors = []
            new_documents = []
            
            # Process each chunk
            for chunk in processing_result.chunks:
                # Generate embedding
                embedding = self.encoder.encode([chunk.content])
                # Normalize for cosine similarity
                embedding = embedding / np.linalg.norm(embedding, axis=1, keepdims=True)
                vectors.append(embedding[0])
                
                # Store document metadata
                doc_metadata = {
                    'chunk_id': chunk.chunk_id,
                    'file_id': processing_result.file_id,
                    'filename': processing_result.metadata.get('filename', ''),
                    'content': chunk.content,
                    'content_type': processing_result.content_type,
                    'chunk_index': chunk.chunk_index,
                    'metadata': chunk.metadata,
                    'timestamp': datetime.utcnow().isoformat()
                }
                new_documents.append(doc_metadata)
            
            if vectors:
                # Add to FAISS index
                vectors_array = np.array(vectors).astype('float32')
                self.index.add(vectors_array)
                
                # Add to documents list
                self.documents.extend(new_documents)
                
                # Save updated index
                await self._save_index()
                
                logger.info(f"Added {len(vectors)} vectors to search index")
                
        except Exception as e:
            logger.error(f"Error adding documents to index: {str(e)}")
            raise
    
    async def search(
        self, 
        query: str, 
        file_contexts: Optional[List[ProcessingResult]] = None,
        limit: int = 10, 
        threshold: float = 0.7
    ) -> List[SearchResult]:
        """
        Perform similarity search
        
        Args:
            query: Search query string
            file_contexts: Optional file contexts for enhanced search
            limit: Maximum number of results
            threshold: Similarity threshold
            
        Returns:
            List of search results
        """
        try:
            if not self.initialized:
                raise Exception("Search service not initialized")
            
            start_time = datetime.now()
            
            # Combine query with file contexts if provided
            enhanced_query = query
            if file_contexts:
                context_texts = []
                for context in file_contexts:
                    if context.text_content:
                        context_texts.append(context.text_content[:500])  # Limit context length
                
                if context_texts:
                    enhanced_query = f"{query} Context: {' '.join(context_texts)}"
            
            # Generate query embedding
            query_embedding = self.encoder.encode([enhanced_query])
            query_embedding = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)
            
            # Search in FAISS index
            if self.index.ntotal == 0:
                return []
            
            # Search for more results initially to filter by threshold
            search_limit = min(limit * 2, self.index.ntotal)
            scores, indices = self.index.search(query_embedding.astype('float32'), search_limit)
            
            # Filter results by threshold and format
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if score >= threshold and idx < len(self.documents):
                    doc = self.documents[idx]
                    
                    result = SearchResult(
                        content=doc['content'],
                        score=float(score),
                        file_id=doc['file_id'],
                        filename=doc['filename'],
                        chunk_id=doc['chunk_id'],
                        metadata=doc['metadata'],
                        content_type=doc['content_type']
                    )
                    results.append(result)
                    
                    if len(results) >= limit:
                        break
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Add processing time to first result if available
            if results:
                if not results[0].metadata:
                    results[0].metadata = {}
                results[0].metadata['processing_time'] = processing_time
            
            logger.info(f"Search completed: {len(results)} results in {processing_time:.3f}s")
            return results
            
        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            raise
    
    async def delete_file_documents(self, file_id: str) -> bool:
        """Delete all documents for a specific file"""
        try:
            if not self.initialized:
                raise Exception("Search service not initialized")
            
            # Find documents to delete
            docs_to_keep = []
            deleted_count = 0
            
            for i, doc in enumerate(self.documents):
                if doc['file_id'] != file_id:
                    docs_to_keep.append(doc)
                else:
                    deleted_count += 1
            
            if deleted_count > 0:
                # Rebuild index with remaining documents
                self.documents = docs_to_keep
                await self._rebuild_index()
                
                logger.info(f"Deleted {deleted_count} documents for file {file_id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error deleting file documents: {str(e)}")
            raise
    
    async def _rebuild_index(self):
        """Rebuild the FAISS index"""
        try:
            # Create new index
            self.index = faiss.IndexFlatIP(self.settings.VECTOR_DIM)
            
            if self.documents:
                # Re-encode all documents
                vectors = []
                for doc in self.documents:
                    embedding = self.encoder.encode([doc['content']])
                    embedding = embedding / np.linalg.norm(embedding, axis=1, keepdims=True)
                    vectors.append(embedding[0])
                
                # Add to index
                vectors_array = np.array(vectors).astype('float32')
                self.index.add(vectors_array)
            
            # Save updated index
            await self._save_index()
            
            logger.info("Index rebuilt successfully")
            
        except Exception as e:
            logger.error(f"Error rebuilding index: {str(e)}")
            raise
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get search index statistics"""
        try:
            total_docs = len(self.documents)
            file_types = {}
            files = set()
            
            for doc in self.documents:
                content_type = doc.get('content_type', 'unknown')
                file_types[content_type] = file_types.get(content_type, 0) + 1
                files.add(doc.get('file_id', ''))
            
            return {
                'total_documents': total_docs,
                'total_files': len(files),
                'index_size': self.index.ntotal if self.index else 0,
                'file_types': file_types,
                'embedding_model': self.settings.EMBEDDING_MODEL,
                'vector_dimension': self.settings.VECTOR_DIM
            }
            
        except Exception as e:
            logger.error(f"Error getting stats: {str(e)}")
            return {}
    
    async def health_check(self) -> ServiceStatus:
        """Check service health"""
        try:
            status = "healthy" if self.initialized and self.encoder is not None else "unhealthy"
            
            details = {
                'initialized': self.initialized,
                'model_loaded': self.encoder is not None,
                'index_size': self.index.ntotal if self.index else 0,
                'documents_count': len(self.documents)
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
            if self.index:
                await self._save_index()
            logger.info("Search service cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
    
    def get_similar_queries(self, query: str, limit: int = 5) -> List[str]:
        """Get similar queries based on document content"""
        # This is a placeholder for query suggestion functionality
        # Could be implemented using query logs or document analysis
        return []
