"""
Cache service for ConfluxAI using Redis for performance optimization
Handles search result caching, embedding caching, and general purpose caching
"""
import json
import pickle
import hashlib
import logging
from typing import Any, Optional, List, Dict
from datetime import datetime, timedelta

try:
    import redis
except ImportError:
    redis = None

from models.schemas import SearchResult, ProcessingResult
from config.settings import Settings

logger = logging.getLogger(__name__)

class CacheService:
    """Redis-based caching service for performance optimization"""
    
    def __init__(self):
        self.settings = Settings()
        self.redis_client = None
        self.initialized = False
        self.cache_prefix = "conflux_ai"
    
    async def initialize(self):
        """Initialize Redis connection"""
        try:
            if not redis:
                logger.warning("Redis not available, caching disabled")
                return
            
            logger.info("Initializing cache service...")
            
            # Create Redis connection
            self.redis_client = redis.Redis(
                host=self.settings.REDIS_HOST,
                port=self.settings.REDIS_PORT,
                db=self.settings.REDIS_DB,
                password=self.settings.REDIS_PASSWORD if self.settings.REDIS_PASSWORD else None,
                decode_responses=False,  # We'll handle encoding manually
                socket_timeout=5,
                socket_connect_timeout=5
            )
            
            # Test connection
            await self._test_connection()
            
            self.initialized = True
            logger.info("Cache service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize cache service: {str(e)}")
            # Don't raise exception, just disable caching
            self.redis_client = None
    
    async def _test_connection(self):
        """Test Redis connection"""
        try:
            self.redis_client.ping()
            logger.info("Redis connection test successful")
        except Exception as e:
            logger.error(f"Redis connection test failed: {str(e)}")
            raise
    
    def _generate_cache_key(self, prefix: str, *args) -> str:
        """Generate cache key from prefix and arguments"""
        # Create hash from arguments
        combined = json.dumps(args, sort_keys=True, default=str)
        hash_key = hashlib.md5(combined.encode()).hexdigest()
        return f"{self.cache_prefix}:{prefix}:{hash_key}"
    
    async def cache_search_results(
        self, 
        query: str, 
        results: List[SearchResult], 
        search_params: Dict[str, Any] = None,
        ttl: int = None
    ) -> bool:
        """Cache search results"""
        try:
            if not self.initialized or not self.redis_client:
                return False
            
            ttl = ttl or self.settings.SEARCH_CACHE_TTL
            cache_key = self._generate_cache_key("search", query, search_params or {})
            
            # Serialize results
            cached_data = {
                'query': query,
                'results': [result.dict() for result in results],
                'search_params': search_params,
                'cached_at': datetime.utcnow().isoformat(),
                'ttl': ttl
            }
            
            # Store in Redis
            serialized_data = pickle.dumps(cached_data)
            self.redis_client.setex(cache_key, ttl, serialized_data)
            
            logger.debug(f"Cached search results for query: {query[:50]}...")
            return True
            
        except Exception as e:
            logger.error(f"Error caching search results: {str(e)}")
            return False
    
    async def get_cached_search_results(
        self, 
        query: str, 
        search_params: Dict[str, Any] = None
    ) -> Optional[List[SearchResult]]:
        """Retrieve cached search results"""
        try:
            if not self.initialized or not self.redis_client:
                return None
            
            cache_key = self._generate_cache_key("search", query, search_params or {})
            
            # Get from Redis
            cached_data = self.redis_client.get(cache_key)
            if not cached_data:
                return None
            
            # Deserialize data
            data = pickle.loads(cached_data)
            
            # Convert back to SearchResult objects
            results = [SearchResult(**result_data) for result_data in data['results']]
            
            logger.debug(f"Retrieved cached search results for query: {query[:50]}...")
            return results
            
        except Exception as e:
            logger.error(f"Error retrieving cached search results: {str(e)}")
            return None
    
    async def cache_embeddings(
        self, 
        text: str, 
        model_name: str, 
        embeddings: List[float],
        ttl: int = 86400  # 24 hours default
    ) -> bool:
        """Cache text embeddings"""
        try:
            if not self.initialized or not self.redis_client:
                return False
            
            cache_key = self._generate_cache_key("embeddings", text, model_name)
            
            cached_data = {
                'text': text,
                'model_name': model_name,
                'embeddings': embeddings,
                'cached_at': datetime.utcnow().isoformat()
            }
            
            serialized_data = pickle.dumps(cached_data)
            self.redis_client.setex(cache_key, ttl, serialized_data)
            
            logger.debug(f"Cached embeddings for text: {text[:50]}...")
            return True
            
        except Exception as e:
            logger.error(f"Error caching embeddings: {str(e)}")
            return False
    
    async def get_cached_embeddings(
        self, 
        text: str, 
        model_name: str
    ) -> Optional[List[float]]:
        """Retrieve cached embeddings"""
        try:
            if not self.initialized or not self.redis_client:
                return None
            
            cache_key = self._generate_cache_key("embeddings", text, model_name)
            
            cached_data = self.redis_client.get(cache_key)
            if not cached_data:
                return None
            
            data = pickle.loads(cached_data)
            return data['embeddings']
            
        except Exception as e:
            logger.error(f"Error retrieving cached embeddings: {str(e)}")
            return None
    
    async def cache_file_processing_result(
        self, 
        file_path: str, 
        file_hash: str, 
        result: ProcessingResult,
        ttl: int = 3600  # 1 hour default
    ) -> bool:
        """Cache file processing results"""
        try:
            if not self.initialized or not self.redis_client:
                return False
            
            cache_key = self._generate_cache_key("file_processing", file_path, file_hash)
            
            cached_data = {
                'file_path': file_path,
                'file_hash': file_hash,
                'result': result.dict(),
                'cached_at': datetime.utcnow().isoformat()
            }
            
            serialized_data = pickle.dumps(cached_data)
            self.redis_client.setex(cache_key, ttl, serialized_data)
            
            logger.debug(f"Cached file processing result for: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error caching file processing result: {str(e)}")
            return False
    
    async def get_cached_file_processing_result(
        self, 
        file_path: str, 
        file_hash: str
    ) -> Optional[ProcessingResult]:
        """Retrieve cached file processing result"""
        try:
            if not self.initialized or not self.redis_client:
                return None
            
            cache_key = self._generate_cache_key("file_processing", file_path, file_hash)
            
            cached_data = self.redis_client.get(cache_key)
            if not cached_data:
                return None
            
            data = pickle.loads(cached_data)
            return ProcessingResult(**data['result'])
            
        except Exception as e:
            logger.error(f"Error retrieving cached file processing result: {str(e)}")
            return None
    
    async def cache_generic(
        self, 
        key: str, 
        data: Any, 
        ttl: int = 3600
    ) -> bool:
        """Cache generic data"""
        try:
            if not self.initialized or not self.redis_client:
                return False
            
            cache_key = self._generate_cache_key("generic", key)
            
            cached_data = {
                'data': data,
                'cached_at': datetime.utcnow().isoformat()
            }
            
            serialized_data = pickle.dumps(cached_data)
            self.redis_client.setex(cache_key, ttl, serialized_data)
            
            logger.debug(f"Cached generic data with key: {key}")
            return True
            
        except Exception as e:
            logger.error(f"Error caching generic data: {str(e)}")
            return False
    
    async def get_cached_generic(self, key: str) -> Optional[Any]:
        """Retrieve cached generic data"""
        try:
            if not self.initialized or not self.redis_client:
                return None
            
            cache_key = self._generate_cache_key("generic", key)
            
            cached_data = self.redis_client.get(cache_key)
            if not cached_data:
                return None
            
            data = pickle.loads(cached_data)
            return data['data']
            
        except Exception as e:
            logger.error(f"Error retrieving cached generic data: {str(e)}")
            return None
    
    async def invalidate_cache_pattern(self, pattern: str) -> int:
        """Invalidate cache entries matching pattern"""
        try:
            if not self.initialized or not self.redis_client:
                return 0
            
            pattern_key = f"{self.cache_prefix}:{pattern}*"
            keys = self.redis_client.keys(pattern_key)
            
            if keys:
                deleted = self.redis_client.delete(*keys)
                logger.info(f"Invalidated {deleted} cache entries matching pattern: {pattern}")
                return deleted
            
            return 0
            
        except Exception as e:
            logger.error(f"Error invalidating cache pattern: {str(e)}")
            return 0
    
    async def invalidate_file_cache(self, file_id: str) -> int:
        """Invalidate all cache entries related to a file"""
        try:
            deleted = 0
            
            # Invalidate search caches (might contain results from this file)
            deleted += await self.invalidate_cache_pattern("search")
            
            # Invalidate file processing cache
            deleted += await self.invalidate_cache_pattern(f"file_processing:*{file_id}*")
            
            logger.info(f"Invalidated {deleted} cache entries for file: {file_id}")
            return deleted
            
        except Exception as e:
            logger.error(f"Error invalidating file cache: {str(e)}")
            return 0
    
    async def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        try:
            if not self.initialized or not self.redis_client:
                return {"status": "disabled", "reason": "Redis not available"}
            
            info = self.redis_client.info()
            
            # Get key counts by pattern
            key_patterns = ["search", "embeddings", "file_processing", "generic"]
            key_counts = {}
            
            for pattern in key_patterns:
                pattern_key = f"{self.cache_prefix}:{pattern}*"
                keys = self.redis_client.keys(pattern_key)
                key_counts[pattern] = len(keys)
            
            stats = {
                "status": "active",
                "redis_info": {
                    "used_memory": info.get('used_memory_human', 'N/A'),
                    "connected_clients": info.get('connected_clients', 0),
                    "total_commands_processed": info.get('total_commands_processed', 0),
                    "keyspace_hits": info.get('keyspace_hits', 0),
                    "keyspace_misses": info.get('keyspace_misses', 0)
                },
                "cache_keys": key_counts,
                "total_keys": sum(key_counts.values())
            }
            
            # Calculate hit rate
            hits = info.get('keyspace_hits', 0)
            misses = info.get('keyspace_misses', 0)
            if hits + misses > 0:
                stats['hit_rate'] = hits / (hits + misses)
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting cache stats: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    async def cleanup(self):
        """Cleanup cache service"""
        try:
            if self.redis_client:
                # Close Redis connection
                self.redis_client.close()
                logger.info("Cache service cleanup completed")
        except Exception as e:
            logger.error(f"Error during cache cleanup: {str(e)}")
    
    def calculate_file_hash(self, file_path: str) -> str:
        """Calculate hash for file content (for cache keys)"""
        try:
            import hashlib
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logger.error(f"Error calculating file hash: {str(e)}")
            return ""
