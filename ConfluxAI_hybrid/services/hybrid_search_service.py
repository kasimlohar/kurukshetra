"""
Hybrid search service combining semantic and keyword search for ConfluxAI
Implements BM25 keyword search alongside vector-based semantic search
"""
import logging
from typing import List, Dict, Any, Optional
import asyncio
from datetime import datetime
import numpy as np

# BM25 keyword search
try:
    from rank_bm25 import BM25Okapi
except ImportError:
    BM25Okapi = None

from models.schemas import SearchResult, HybridSearchRequest, SearchFacets, EnhancedSearchResponse
from services.search_service import SearchService
from config.settings import Settings

logger = logging.getLogger(__name__)

class HybridSearchService:
    """Combines semantic and keyword search for better results"""
    
    def __init__(self, search_service: SearchService):
        self.settings = Settings()
        self.search_service = search_service
        self.bm25_index = None
        self.documents_for_bm25 = []
        self.document_metadata = []
        self.initialized = False
    
    async def initialize(self):
        """Initialize the hybrid search service"""
        try:
            logger.info("Initializing hybrid search service...")
            
            if not BM25Okapi:
                logger.warning("rank-bm25 not available, hybrid search will use semantic search only")
                self.initialized = True
                return
            
            # Build BM25 index from existing documents
            await self._build_bm25_index()
            
            self.initialized = True
            logger.info("Hybrid search service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize hybrid search service: {str(e)}")
            raise
    
    async def _build_bm25_index(self):
        """Build BM25 index from existing documents"""
        try:
            if not self.search_service.initialized or not self.search_service.documents:
                logger.info("No documents available for BM25 indexing")
                return
            
            # Extract text content and metadata
            corpus = []
            self.documents_for_bm25 = []
            self.document_metadata = []
            
            for doc in self.search_service.documents:
                content = doc.get('content', '')
                if content:
                    # Tokenize content for BM25
                    tokens = self._tokenize_text(content)
                    corpus.append(tokens)
                    self.documents_for_bm25.append(content)
                    self.document_metadata.append(doc)
            
            if corpus:
                self.bm25_index = BM25Okapi(corpus)
                logger.info(f"Built BM25 index with {len(corpus)} documents")
            
        except Exception as e:
            logger.error(f"Error building BM25 index: {str(e)}")
            raise
    
    def _tokenize_text(self, text: str) -> List[str]:
        """Simple tokenization for BM25"""
        import re
        # Simple word tokenization, lowercased
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens
    
    async def hybrid_search(self, request: HybridSearchRequest) -> EnhancedSearchResponse:
        """
        Perform hybrid search combining semantic and keyword search
        
        Args:
            request: Hybrid search request with parameters
            
        Returns:
            Enhanced search response with combined results
        """
        try:
            start_time = datetime.now()
            
            if not self.initialized:
                raise Exception("Hybrid search service not initialized")
            
            # Get semantic search results
            semantic_results = await self._get_semantic_results(request)
            
            # Get keyword search results
            keyword_results = await self._get_keyword_results(request)
            
            # Combine and rank results
            combined_results = self._combine_results(
                semantic_results, 
                keyword_results, 
                request.semantic_weight, 
                request.keyword_weight
            )
            
            # Apply filters
            filtered_results = self._apply_filters(combined_results, request)
            
            # Sort results
            sorted_results = self._sort_results(filtered_results, request.sort_by)
            
            # Limit results
            limited_results = sorted_results[:request.limit]
            
            # Generate facets if requested
            facets = None
            if request.facets:
                facets = self._generate_facets(filtered_results)
            
            # Generate suggestions
            suggestions = self._generate_suggestions(request.query, limited_results)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return EnhancedSearchResponse(
                query=request.query,
                results=limited_results,
                total_results=len(filtered_results),
                processing_time=processing_time,
                suggestions=suggestions,
                facets=facets,
                search_type="hybrid" if self.bm25_index else "semantic"
            )
            
        except Exception as e:
            logger.error(f"Hybrid search failed: {str(e)}")
            raise
    
    async def _get_semantic_results(self, request: HybridSearchRequest) -> List[SearchResult]:
        """Get semantic search results"""
        try:
            return await self.search_service.search(
                query=request.query,
                file_contexts=None,
                limit=request.limit * 2,  # Get more results for combination
                threshold=request.threshold
            )
        except Exception as e:
            logger.error(f"Semantic search failed: {str(e)}")
            return []
    
    async def _get_keyword_results(self, request: HybridSearchRequest) -> List[SearchResult]:
        """Get keyword search results using BM25"""
        try:
            if not self.bm25_index or not self.documents_for_bm25:
                return []
            
            # Tokenize query
            query_tokens = self._tokenize_text(request.query)
            
            # Get BM25 scores
            scores = self.bm25_index.get_scores(query_tokens)
            
            # Create results with scores
            results = []
            for i, score in enumerate(scores):
                if score > 0 and i < len(self.document_metadata):  # Only include non-zero scores
                    doc = self.document_metadata[i]
                    
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
            
            # Sort by score and limit
            results.sort(key=lambda x: x.score, reverse=True)
            return results[:request.limit * 2]
            
        except Exception as e:
            logger.error(f"Keyword search failed: {str(e)}")
            return []
    
    def _combine_results(
        self, 
        semantic_results: List[SearchResult], 
        keyword_results: List[SearchResult], 
        semantic_weight: float, 
        keyword_weight: float
    ) -> List[SearchResult]:
        """Combine semantic and keyword search results"""
        try:
            # Normalize weights
            total_weight = semantic_weight + keyword_weight
            if total_weight > 0:
                semantic_weight = semantic_weight / total_weight
                keyword_weight = keyword_weight / total_weight
            else:
                semantic_weight = 0.7
                keyword_weight = 0.3
            
            # Create combined results map
            combined_map = {}
            
            # Add semantic results
            for result in semantic_results:
                key = result.chunk_id or f"{result.file_id}_{hash(result.content[:100])}"
                combined_map[key] = {
                    'result': result,
                    'semantic_score': result.score,
                    'keyword_score': 0.0
                }
            
            # Add keyword results
            for result in keyword_results:
                key = result.chunk_id or f"{result.file_id}_{hash(result.content[:100])}"
                if key in combined_map:
                    combined_map[key]['keyword_score'] = result.score
                else:
                    combined_map[key] = {
                        'result': result,
                        'semantic_score': 0.0,
                        'keyword_score': result.score
                    }
            
            # Calculate combined scores
            combined_results = []
            for key, data in combined_map.items():
                # Normalize scores (simple min-max normalization)
                semantic_score_norm = min(data['semantic_score'], 1.0)
                keyword_score_norm = min(data['keyword_score'] / 10.0, 1.0) if data['keyword_score'] > 0 else 0.0
                
                # Calculate weighted combined score
                combined_score = (semantic_weight * semantic_score_norm + 
                                keyword_weight * keyword_score_norm)
                
                # Update result with combined score
                result = data['result']
                result.score = combined_score
                
                # Add scoring details to metadata
                if not result.metadata:
                    result.metadata = {}
                result.metadata.update({
                    'semantic_score': data['semantic_score'],
                    'keyword_score': data['keyword_score'],
                    'combined_score': combined_score,
                    'search_type': 'hybrid'
                })
                
                combined_results.append(result)
            
            # Sort by combined score
            combined_results.sort(key=lambda x: x.score, reverse=True)
            return combined_results
            
        except Exception as e:
            logger.error(f"Error combining results: {str(e)}")
            # Fallback to semantic results
            return semantic_results
    
    def _apply_filters(self, results: List[SearchResult], request: HybridSearchRequest) -> List[SearchResult]:
        """Apply filters to search results"""
        filtered_results = results
        
        try:
            # Filter by file types
            if request.file_types:
                filtered_results = [
                    r for r in filtered_results 
                    if any(r.filename and r.filename.lower().endswith(f'.{ft.lower()}') 
                          for ft in request.file_types)
                ]
            
            # Filter by content types
            if request.content_types:
                filtered_results = [
                    r for r in filtered_results 
                    if r.content_type in request.content_types
                ]
            
            # Filter by date range (if metadata contains dates)
            if request.date_from or request.date_to:
                # This would require date information in metadata
                # Implementation depends on how dates are stored
                pass
            
            # Apply metadata filters
            if request.metadata_filters:
                for key, value in request.metadata_filters.items():
                    filtered_results = [
                        r for r in filtered_results 
                        if r.metadata and r.metadata.get(key) == value
                    ]
            
            # Apply threshold filter
            filtered_results = [
                r for r in filtered_results 
                if r.score >= request.threshold
            ]
            
            return filtered_results
            
        except Exception as e:
            logger.error(f"Error applying filters: {str(e)}")
            return results
    
    def _sort_results(self, results: List[SearchResult], sort_by: str) -> List[SearchResult]:
        """Sort results by specified criteria"""
        try:
            if sort_by == "relevance":
                return sorted(results, key=lambda x: x.score, reverse=True)
            elif sort_by == "date":
                # Sort by date if available in metadata
                return sorted(results, key=lambda x: x.metadata.get('upload_time', ''), reverse=True)
            elif sort_by == "filename":
                return sorted(results, key=lambda x: x.filename or '', reverse=False)
            else:
                return results
        except Exception as e:
            logger.error(f"Error sorting results: {str(e)}")
            return results
    
    def _generate_facets(self, results: List[SearchResult]) -> SearchFacets:
        """Generate facets from search results"""
        try:
            file_types = {}
            content_types = {}
            authors = {}
            
            for result in results:
                # File type facets
                if result.filename:
                    ext = result.filename.split('.')[-1].lower()
                    file_types[ext] = file_types.get(ext, 0) + 1
                
                # Content type facets
                content_types[result.content_type] = content_types.get(result.content_type, 0) + 1
                
                # Author facets (if available in metadata)
                if result.metadata and 'author' in result.metadata:
                    author = result.metadata['author']
                    authors[author] = authors.get(author, 0) + 1
            
            return SearchFacets(
                file_types=file_types,
                content_types=content_types,
                date_ranges={},  # Would implement based on available date data
                authors=authors
            )
            
        except Exception as e:
            logger.error(f"Error generating facets: {str(e)}")
            return SearchFacets()
    
    def _generate_suggestions(self, query: str, results: List[SearchResult]) -> List[str]:
        """Generate query suggestions based on results"""
        try:
            suggestions = []
            
            # Simple suggestions based on common terms in results
            if results:
                # Extract frequent terms from top results
                all_content = " ".join([r.content[:200] for r in results[:5]])
                terms = self._tokenize_text(all_content)
                
                # Find terms not in original query
                query_terms = set(self._tokenize_text(query))
                common_terms = {}
                
                for term in terms:
                    if term not in query_terms and len(term) > 3:
                        common_terms[term] = common_terms.get(term, 0) + 1
                
                # Get top terms
                sorted_terms = sorted(common_terms.items(), key=lambda x: x[1], reverse=True)
                suggestions = [f"{query} {term}" for term, _ in sorted_terms[:3]]
            
            return suggestions[:5]
            
        except Exception as e:
            logger.error(f"Error generating suggestions: {str(e)}")
            return []
    
    async def update_bm25_index(self, new_documents: List[Dict[str, Any]]):
        """Update BM25 index with new documents"""
        try:
            if not BM25Okapi:
                return
            
            # Add new documents to existing ones
            for doc in new_documents:
                content = doc.get('content', '')
                if content:
                    tokens = self._tokenize_text(content)
                    self.documents_for_bm25.append(content)
                    self.document_metadata.append(doc)
            
            # Rebuild BM25 index
            if self.documents_for_bm25:
                corpus = [self._tokenize_text(doc) for doc in self.documents_for_bm25]
                self.bm25_index = BM25Okapi(corpus)
                logger.info(f"Updated BM25 index with {len(self.documents_for_bm25)} total documents")
            
        except Exception as e:
            logger.error(f"Error updating BM25 index: {str(e)}")
    
    async def remove_from_bm25_index(self, file_id: str):
        """Remove documents from BM25 index by file_id"""
        try:
            if not self.bm25_index:
                return
            
            # Remove documents matching file_id
            new_documents = []
            new_metadata = []
            
            for i, doc in enumerate(self.document_metadata):
                if doc.get('file_id') != file_id:
                    new_documents.append(self.documents_for_bm25[i])
                    new_metadata.append(doc)
            
            self.documents_for_bm25 = new_documents
            self.document_metadata = new_metadata
            
            # Rebuild index
            if self.documents_for_bm25:
                corpus = [self._tokenize_text(doc) for doc in self.documents_for_bm25]
                self.bm25_index = BM25Okapi(corpus)
            else:
                self.bm25_index = None
                
            logger.info(f"Removed documents for file {file_id} from BM25 index")
            
        except Exception as e:
            logger.error(f"Error removing from BM25 index: {str(e)}")
    
    async def health_check(self) -> Dict[str, Any]:
        """Check hybrid search service health"""
        try:
            bm25_status = "available" if BM25Okapi and self.bm25_index else "unavailable"
            search_service_status = "healthy" if self.search_service and self.search_service.initialized else "unhealthy"
            
            document_count = len(self.documents_for_bm25) if self.documents_for_bm25 else 0
            
            return {
                "status": "healthy" if self.initialized else "unhealthy",
                "initialized": self.initialized,
                "bm25_search": bm25_status,
                "semantic_search": search_service_status,
                "indexed_documents": document_count,
                "message": f"Hybrid search service operational with {document_count} documents"
            }
            
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "initialized": False,
                "error": str(e),
                "message": "Hybrid search service health check failed"
            }
