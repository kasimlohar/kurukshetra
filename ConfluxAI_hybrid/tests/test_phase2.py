"""
Test script for ConfluxAI Phase 2 features
Tests enhanced file processing, hybrid search, caching, and background tasks
"""
import asyncio
import aiohttp
import json
import tempfile
import os
from pathlib import Path
import time
import sys

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from config.settings import Settings

BASE_URL = "http://localhost:8000"

class ConfluxAIPhase2Tester:
    """Test suite for ConfluxAI Phase 2 features"""
    
    def __init__(self):
        self.settings = Settings()
        self.session = None
        self.test_results = []
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def test_system_health(self):
        """Test system health endpoint"""
        print("🔍 Testing system health...")
        
        try:
            async with self.session.get(f"{BASE_URL}/system/health") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"   ✅ System status: {data.get('status', 'unknown')}")
                    
                    services = data.get('services', {})
                    for service_name, health in services.items():
                        status = health.get('status', 'unknown')
                        print(f"   📊 {service_name}: {status}")
                    
                    self.test_results.append(("System Health", True, "All services checked"))
                    return True
                else:
                    print(f"   ❌ Health check failed: {response.status}")
                    self.test_results.append(("System Health", False, f"HTTP {response.status}"))
                    return False
                    
        except Exception as e:
            print(f"   ❌ Health check error: {str(e)}")
            self.test_results.append(("System Health", False, str(e)))
            return False
    
    async def test_enhanced_file_processing(self):
        """Test enhanced file processing with Phase 2 features"""
        print("📄 Testing enhanced file processing...")
        
        try:
            # Create a test PDF content
            test_content = """
            # Test Document for Phase 2
            
            This is a test document for ConfluxAI Phase 2 enhanced file processing.
            
            ## Key Features
            - Advanced PDF processing
            - Table extraction
            - Image analysis with object detection
            - Improved OCR confidence scoring
            
            ## Sample Table
            | Feature | Status | Priority |
            |---------|--------|----------|
            | PDF Processing | ✅ Complete | High |
            | Image Analysis | 🔄 In Progress | High |
            | Hybrid Search | ✅ Complete | Medium |
            | Caching | ✅ Complete | Medium |
            
            This document tests the enhanced file processing capabilities.
            """
            
            # Create temporary test file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write(test_content)
                temp_file_path = f.name
            
            try:
                # Test file upload and indexing
                with open(temp_file_path, 'rb') as f:
                    data = aiohttp.FormData()
                    data.add_field('files', f, filename='test_phase2.txt', content_type='text/plain')
                    data.add_field('metadata', json.dumps({'test': 'phase2', 'priority': 'high'}))
                    
                    async with self.session.post(f"{BASE_URL}/index", data=data) as response:
                        if response.status == 200:
                            result = await response.json()
                            indexed_files = result.get('indexed_files', [])
                            
                            if indexed_files:
                                file_id = indexed_files[0].get('file_id')
                                chunks_count = indexed_files[0].get('chunks_indexed', 0)
                                print(f"   ✅ File indexed successfully: {file_id}")
                                print(f"   📊 Chunks created: {chunks_count}")
                                
                                self.test_results.append(("Enhanced File Processing", True, f"File indexed with {chunks_count} chunks"))
                                return file_id
                            else:
                                print("   ❌ No files were indexed")
                                self.test_results.append(("Enhanced File Processing", False, "No files indexed"))
                                return None
                        else:
                            error_detail = await response.text()
                            print(f"   ❌ File indexing failed: {response.status} - {error_detail}")
                            self.test_results.append(("Enhanced File Processing", False, f"HTTP {response.status}"))
                            return None
                            
            finally:
                # Cleanup temp file
                os.unlink(temp_file_path)
                
        except Exception as e:
            print(f"   ❌ Enhanced file processing error: {str(e)}")
            self.test_results.append(("Enhanced File Processing", False, str(e)))
            return None
    
    async def test_hybrid_search(self):
        """Test hybrid search functionality"""
        print("🔍 Testing hybrid search...")
        
        try:
            # Test query
            search_query = "test document phase 2 features"
            
            # Test hybrid search endpoint
            data = aiohttp.FormData()
            data.add_field('query', search_query)
            data.add_field('limit', '5')
            data.add_field('semantic_weight', '0.7')
            data.add_field('keyword_weight', '0.3')
            data.add_field('facets', 'true')
            data.add_field('sort_by', 'relevance')
            
            async with self.session.post(f"{BASE_URL}/search/hybrid", data=data) as response:
                if response.status == 200:
                    result = await response.json()
                    
                    query = result.get('query')
                    results = result.get('results', [])
                    search_type = result.get('search_type', 'unknown')
                    processing_time = result.get('processing_time', 0)
                    facets = result.get('facets')
                    suggestions = result.get('suggestions')
                    
                    print(f"   ✅ Hybrid search completed")
                    print(f"   📊 Query: {query}")
                    print(f"   📊 Results found: {len(results)}")
                    print(f"   📊 Search type: {search_type}")
                    print(f"   📊 Processing time: {processing_time:.3f}s")
                    
                    if facets:
                        print(f"   📊 Facets available: {list(facets.keys())}")
                    
                    if suggestions:
                        print(f"   📊 Suggestions: {len(suggestions)}")
                    
                    # Test individual result details
                    if results:
                        first_result = results[0]
                        score = first_result.get('score', 0)
                        metadata = first_result.get('metadata', {})
                        print(f"   📊 Top result score: {score:.3f}")
                        
                        if 'hybrid_search' in metadata:
                            print(f"   📊 Hybrid search metadata: ✅")
                    
                    self.test_results.append(("Hybrid Search", True, f"Found {len(results)} results in {processing_time:.3f}s"))
                    return True
                else:
                    error_detail = await response.text()
                    print(f"   ❌ Hybrid search failed: {response.status} - {error_detail}")
                    self.test_results.append(("Hybrid Search", False, f"HTTP {response.status}"))
                    return False
                    
        except Exception as e:
            print(f"   ❌ Hybrid search error: {str(e)}")
            self.test_results.append(("Hybrid Search", False, str(e)))
            return False
    
    async def test_search_suggestions(self):
        """Test search suggestions"""
        print("💡 Testing search suggestions...")
        
        try:
            params = {'q': 'test', 'limit': 5}
            
            async with self.session.get(f"{BASE_URL}/search/suggestions", params=params) as response:
                if response.status == 200:
                    result = await response.json()
                    suggestions = result.get('suggestions', [])
                    
                    print(f"   ✅ Suggestions retrieved: {len(suggestions)}")
                    if suggestions:
                        print(f"   📊 Sample suggestions: {suggestions[:3]}")
                    
                    self.test_results.append(("Search Suggestions", True, f"Got {len(suggestions)} suggestions"))
                    return True
                else:
                    print(f"   ❌ Suggestions failed: {response.status}")
                    self.test_results.append(("Search Suggestions", False, f"HTTP {response.status}"))
                    return False
                    
        except Exception as e:
            print(f"   ❌ Suggestions error: {str(e)}")
            self.test_results.append(("Search Suggestions", False, str(e)))
            return False
    
    async def test_batch_processing(self):
        """Test batch file processing"""
        print("📦 Testing batch processing...")
        
        try:
            # Create multiple test files
            test_files = []
            temp_files = []
            
            for i in range(3):
                content = f"""
                Test File {i+1} for Batch Processing
                
                This is test file number {i+1} created for testing the batch processing
                functionality in ConfluxAI Phase 2.
                
                Content: Batch processing test file {i+1}
                Keywords: batch, processing, test, file{i+1}
                """
                
                temp_file = tempfile.NamedTemporaryFile(mode='w', suffix=f'_batch_{i+1}.txt', delete=False)
                temp_file.write(content)
                temp_file.close()
                
                temp_files.append(temp_file.name)
                test_files.append((f'test_batch_{i+1}.txt', temp_file.name))
            
            try:
                # Submit batch processing request
                data = aiohttp.FormData()
                
                for filename, filepath in test_files:
                    with open(filepath, 'rb') as f:
                        data.add_field('files', f, filename=filename, content_type='text/plain')
                
                data.add_field('metadata', json.dumps({'batch_test': True, 'phase': 2}))
                data.add_field('async_processing', 'false')  # Use sync for easier testing
                data.add_field('priority', '7')
                
                async with self.session.post(f"{BASE_URL}/index/batch", data=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        
                        task_id = result.get('task_id')
                        status = result.get('status')
                        message = result.get('message')
                        
                        print(f"   ✅ Batch processing completed")
                        print(f"   📊 Task ID: {task_id}")
                        print(f"   📊 Status: {status}")
                        print(f"   📊 Message: {message}")
                        
                        batch_result = result.get('result', {})
                        if batch_result:
                            indexed_files = batch_result.get('indexed_files', [])
                            failed_files = batch_result.get('failed_files', [])
                            
                            print(f"   📊 Files indexed: {len(indexed_files)}")
                            print(f"   📊 Files failed: {len(failed_files)}")
                        
                        self.test_results.append(("Batch Processing", True, f"Processed {len(test_files)} files"))
                        return True
                    else:
                        error_detail = await response.text()
                        print(f"   ❌ Batch processing failed: {response.status} - {error_detail}")
                        self.test_results.append(("Batch Processing", False, f"HTTP {response.status}"))
                        return False
                        
            finally:
                # Cleanup temp files
                for temp_file in temp_files:
                    try:
                        os.unlink(temp_file)
                    except:
                        pass
                        
        except Exception as e:
            print(f"   ❌ Batch processing error: {str(e)}")
            self.test_results.append(("Batch Processing", False, str(e)))
            return False
    
    async def test_cache_functionality(self):
        """Test caching functionality"""
        print("🗃️ Testing cache functionality...")
        
        try:
            # Get cache stats
            async with self.session.get(f"{BASE_URL}/cache/stats") as response:
                if response.status == 200:
                    stats = await response.json()
                    
                    status = stats.get('status')
                    total_keys = stats.get('total_keys', 0)
                    cache_keys = stats.get('cache_keys', {})
                    
                    print(f"   ✅ Cache stats retrieved")
                    print(f"   📊 Cache status: {status}")
                    print(f"   📊 Total keys: {total_keys}")
                    
                    if cache_keys:
                        print(f"   📊 Key types: {list(cache_keys.keys())}")
                    
                    # Test cache performance with repeated searches
                    if status in ['active', 'enabled']:
                        await self._test_cache_performance()
                    
                    self.test_results.append(("Cache Functionality", True, f"Status: {status}, Keys: {total_keys}"))
                    return True
                else:
                    print(f"   ❌ Cache stats failed: {response.status}")
                    self.test_results.append(("Cache Functionality", False, f"HTTP {response.status}"))
                    return False
                    
        except Exception as e:
            print(f"   ❌ Cache error: {str(e)}")
            self.test_results.append(("Cache Functionality", False, str(e)))
            return False
    
    async def _test_cache_performance(self):
        """Test cache performance with repeated searches"""
        print("   🚀 Testing cache performance...")
        
        query = "test performance cache"
        
        # First search (should hit database/index)
        start_time = time.time()
        await self._perform_search(query)
        first_search_time = time.time() - start_time
        
        # Second search (should hit cache)
        start_time = time.time()
        await self._perform_search(query)
        second_search_time = time.time() - start_time
        
        print(f"   📊 First search: {first_search_time:.3f}s")
        print(f"   📊 Second search: {second_search_time:.3f}s")
        
        if second_search_time < first_search_time:
            speedup = first_search_time / second_search_time
            print(f"   📊 Cache speedup: {speedup:.1f}x")
        
    async def _perform_search(self, query):
        """Helper method to perform a search"""
        data = aiohttp.FormData()
        data.add_field('query', query)
        data.add_field('limit', '5')
        
        async with self.session.post(f"{BASE_URL}/search", data=data) as response:
            return await response.json() if response.status == 200 else None
    
    async def test_performance_metrics(self):
        """Test performance metrics endpoint"""
        print("📈 Testing performance metrics...")
        
        try:
            async with self.session.get(f"{BASE_URL}/system/metrics") as response:
                if response.status == 200:
                    metrics = await response.json()
                    
                    search_time = metrics.get('search_response_time_avg', 0)
                    processing_time = metrics.get('file_processing_time_avg', 0)
                    cache_hit_rate = metrics.get('cache_hit_rate', 0)
                    
                    print(f"   ✅ Performance metrics retrieved")
                    print(f"   📊 Avg search time: {search_time}ms")
                    print(f"   📊 Avg processing time: {processing_time}ms")
                    print(f"   📊 Cache hit rate: {cache_hit_rate}%")
                    
                    self.test_results.append(("Performance Metrics", True, f"Search: {search_time}ms"))
                    return True
                else:
                    print(f"   ❌ Performance metrics failed: {response.status}")
                    self.test_results.append(("Performance Metrics", False, f"HTTP {response.status}"))
                    return False
                    
        except Exception as e:
            print(f"   ❌ Performance metrics error: {str(e)}")
            self.test_results.append(("Performance Metrics", False, str(e)))
            return False
    
    async def run_all_tests(self):
        """Run all Phase 2 tests"""
        print("🚀 ConfluxAI Phase 2 Test Suite")
        print("=" * 50)
        
        # Test order matters - some tests depend on previous ones
        tests = [
            ("System Health", self.test_system_health),
            ("Enhanced File Processing", self.test_enhanced_file_processing),
            ("Hybrid Search", self.test_hybrid_search),
            ("Search Suggestions", self.test_search_suggestions),
            ("Batch Processing", self.test_batch_processing),
            ("Cache Functionality", self.test_cache_functionality),
            ("Performance Metrics", self.test_performance_metrics),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                result = await test_func()
                if result:
                    passed += 1
            except Exception as e:
                print(f"   ❌ {test_name} failed with exception: {str(e)}")
                self.test_results.append((test_name, False, f"Exception: {str(e)}"))
            
            print()  # Add spacing between tests
        
        # Print summary
        print("📊 Test Summary")
        print("=" * 50)
        print(f"Tests passed: {passed}/{total}")
        print(f"Success rate: {(passed/total)*100:.1f}%")
        print()
        
        # Detailed results
        print("📋 Detailed Results")
        print("-" * 50)
        for test_name, success, details in self.test_results:
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status} {test_name}: {details}")
        
        return passed == total

async def main():
    """Main test function"""
    print("ConfluxAI Phase 2 Feature Test Suite")
    print("Make sure the ConfluxAI server is running on http://localhost:8000")
    print()
    
    # Wait a moment for user to read
    await asyncio.sleep(1)
    
    async with ConfluxAIPhase2Tester() as tester:
        success = await tester.run_all_tests()
        
        if success:
            print("\n🎉 All tests passed! ConfluxAI Phase 2 is working correctly.")
            return 0
        else:
            print("\n⚠️ Some tests failed. Check the detailed results above.")
            return 1

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        exit(exit_code)
    except KeyboardInterrupt:
        print("\n❌ Tests interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n❌ Test suite failed: {str(e)}")
        exit(1)
