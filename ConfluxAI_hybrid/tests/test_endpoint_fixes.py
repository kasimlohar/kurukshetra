#!/usr/bin/env python3
"""
Test script to verify the hybrid search endpoint fixes
"""

import asyncio
import aiohttp
import json

async def test_hybrid_search_json():
    """Test hybrid search with JSON payload"""
    
    print("🧪 Testing Hybrid Search with JSON payload...")
    
    try:
        async with aiohttp.ClientSession() as session:
            # Test data
            search_data = {
                "query": "machine learning algorithms",
                "semantic_weight": 0.7,
                "keyword_weight": 0.3,
                "limit": 10,
                "facets": True
            }
            
            # Test JSON request
            headers = {"Content-Type": "application/json"}
            
            async with session.post(
                "http://localhost:8000/search/hybrid", 
                json=search_data,
                headers=headers
            ) as resp:
                
                print(f"Status: {resp.status}")
                response_text = await resp.text()
                print(f"Response: {response_text[:200]}...")
                
                if resp.status == 200:
                    result = await resp.json()
                    print("✅ JSON request successful!")
                    print(f"   Query: {result.get('query')}")
                    print(f"   Results: {len(result.get('results', []))}")
                    print(f"   Search Type: {result.get('search_type')}")
                else:
                    print(f"❌ JSON request failed: {resp.status}")
                    
    except Exception as e:
        print(f"❌ Test failed: {e}")

async def test_hybrid_search_form():
    """Test hybrid search with form data"""
    
    print("\n🧪 Testing Hybrid Search with Form data...")
    
    try:
        async with aiohttp.ClientSession() as session:
            # Test form data
            data = aiohttp.FormData()
            data.add_field('query', 'data analysis algorithms')
            data.add_field('semantic_weight', '0.6')
            data.add_field('keyword_weight', '0.4')
            data.add_field('limit', '5')
            data.add_field('facets', 'true')
            
            async with session.post(
                "http://localhost:8000/search/hybrid", 
                data=data
            ) as resp:
                
                print(f"Status: {resp.status}")
                response_text = await resp.text()
                print(f"Response: {response_text[:200]}...")
                
                if resp.status == 200:
                    result = await resp.json()
                    print("✅ Form request successful!")
                    print(f"   Query: {result.get('query')}")
                    print(f"   Results: {len(result.get('results', []))}")
                    print(f"   Search Type: {result.get('search_type')}")
                else:
                    print(f"❌ Form request failed: {resp.status}")
                    
    except Exception as e:
        print(f"❌ Test failed: {e}")

async def test_system_health():
    """Test system health endpoint"""
    
    print("\n🏥 Testing System Health...")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:8000/system/health") as resp:
                
                print(f"Status: {resp.status}")
                
                if resp.status == 200:
                    result = await resp.json()
                    print("✅ Health check successful!")
                    print(f"   Overall Status: {result.get('status')}")
                    
                    services = result.get('services', {})
                    for service_name, service_info in services.items():
                        status = service_info.get('status', 'unknown')
                        print(f"   {service_name}: {status}")
                else:
                    response_text = await resp.text()
                    print(f"❌ Health check failed: {resp.status}")
                    print(f"   Response: {response_text}")
                    
    except Exception as e:
        print(f"❌ Health check test failed: {e}")

async def main():
    """Run all tests"""
    print("🚀 ConfluxAI Phase 2 - Endpoint Fix Testing")
    print("=" * 50)
    
    # Test server connectivity first
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:8000/docs") as resp:
                if resp.status == 200:
                    print("✅ Server is running and accessible")
                else:
                    print("❌ Server may not be running properly")
                    return
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("Please ensure the server is running with: python main.py")
        return
    
    # Run tests
    await test_system_health()
    await test_hybrid_search_json()
    await test_hybrid_search_form()
    
    print("\n🎉 Testing Complete!")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
