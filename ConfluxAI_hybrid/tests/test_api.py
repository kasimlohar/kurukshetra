"""
Test script for ConfluxAI Multi-Modal Search Agent API
"""
import asyncio
import aiohttp
import json
import os
from pathlib import Path

API_BASE_URL = "http://localhost:8000"

async def test_health_check():
    """Test health check endpoint"""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{API_BASE_URL}/health") as response:
                if response.status == 200:
                    data = await response.json()
                    print("✅ Health check passed")
                    print(f"   Status: {data.get('status')}")
                    return True
                else:
                    print(f"❌ Health check failed: {response.status}")
                    return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False

async def test_search():
    """Test search endpoint"""
    async with aiohttp.ClientSession() as session:
        try:
            # Test search without files
            data = aiohttp.FormData()
            data.add_field('query', 'machine learning')
            data.add_field('limit', '5')
            data.add_field('threshold', '0.5')
            
            async with session.post(f"{API_BASE_URL}/search", data=data) as response:
                if response.status == 200:
                    result = await response.json()
                    print("✅ Search test passed")
                    print(f"   Query: {result.get('query')}")
                    print(f"   Results: {result.get('total_results')}")
                    return True
                else:
                    text = await response.text()
                    print(f"❌ Search test failed: {response.status}")
                    print(f"   Response: {text}")
                    return False
        except Exception as e:
            print(f"❌ Search test error: {e}")
            return False

async def test_index_stats():
    """Test index stats endpoint"""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{API_BASE_URL}/index/stats") as response:
                if response.status == 200:
                    stats = await response.json()
                    print("✅ Index stats test passed")
                    print(f"   Total files: {stats.get('total_files', 0)}")
                    print(f"   Total chunks: {stats.get('total_chunks', 0)}")
                    return True
                else:
                    text = await response.text()
                    print(f"❌ Index stats test failed: {response.status}")
                    print(f"   Response: {text}")
                    return False
        except Exception as e:
            print(f"❌ Index stats test error: {e}")
            return False

async def test_index_text_file():
    """Test indexing a simple text file"""
    async with aiohttp.ClientSession() as session:
        try:
            # Create a test text file
            test_content = """
            This is a test document for the ConfluxAI Multi-Modal Search Agent.
            It contains information about machine learning, artificial intelligence,
            and natural language processing. The system should be able to index
            this content and make it searchable through vector embeddings.
            """
            
            # Prepare form data
            data = aiohttp.FormData()
            data.add_field('files', test_content, filename='test_document.txt', content_type='text/plain')
            data.add_field('metadata', json.dumps({'test': True, 'category': 'sample'}))
            
            async with session.post(f"{API_BASE_URL}/index", data=data) as response:
                if response.status == 200:
                    result = await response.json()
                    print("✅ Index test passed")
                    print(f"   Success: {result.get('success')}")
                    print(f"   Indexed files: {result.get('total_indexed')}")
                    return True
                else:
                    text = await response.text()
                    print(f"❌ Index test failed: {response.status}")
                    print(f"   Response: {text}")
                    return False
        except Exception as e:
            print(f"❌ Index test error: {e}")
            return False

async def main():
    """Run all tests"""
    print("🚀 Starting ConfluxAI API Tests")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_check),
        ("Search", test_search),
        ("Index Stats", test_index_stats),
        ("Index Text File", test_index_text_file),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        result = await test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the API server and dependencies.")

if __name__ == "__main__":
    print("Note: Make sure the API server is running on http://localhost:8000")
    print("Start the server with: python main.py")
    print()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted by user")
    except Exception as e:
        print(f"🚫 Test runner error: {e}")
