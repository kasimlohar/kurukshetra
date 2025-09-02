"""
Quick test script for ConfluxAI API endpoints with PostgreSQL
"""

import asyncio
import aiohttp
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

async def test_api():
    """Test ConfluxAI API endpoints"""
    
    base_url = f"http://localhost:{os.getenv('PORT', '8000')}"
    
    print(f"""
🧪 ConfluxAI API Test Suite
===========================
Base URL: {base_url}
""")
    
    async with aiohttp.ClientSession() as session:
        
        # Test 1: Health Check
        print("1. Testing Health Endpoint...")
        try:
            async with session.get(f"{base_url}/health") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"   ✅ Health: {data.get('status', 'unknown')}")
                else:
                    print(f"   ❌ Health check failed: {response.status}")
        except Exception as e:
            print(f"   ❌ Health check error: {e}")
        
        # Test 2: Database Health
        print("\n2. Testing Database Health...")
        try:
            async with session.get(f"{base_url}/health/database") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"   ✅ Database: {data.get('status', 'unknown')}")
                    print(f"   📊 Connection: {data.get('connection', 'unknown')}")
                    if 'latency' in data:
                        print(f"   ⚡ Latency: {data['latency']}ms")
                else:
                    print(f"   ❌ Database health failed: {response.status}")
        except Exception as e:
            print(f"   ❌ Database health error: {e}")
        
        # Test 3: Analytics Endpoint
        print("\n3. Testing Analytics Endpoint...")
        try:
            async with session.get(f"{base_url}/analytics") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"   ✅ Analytics: Available")
                    if 'overview' in data:
                        overview = data['overview']
                        print(f"   📊 Total Documents: {overview.get('totalDocuments', 'N/A')}")
                        print(f"   🔍 Total Searches: {overview.get('totalSearches', 'N/A')}")
                else:
                    print(f"   ❌ Analytics failed: {response.status}")
        except Exception as e:
            print(f"   ❌ Analytics error: {e}")
        
        # Test 4: Search Endpoint
        print("\n4. Testing Search Endpoint...")
        try:
            search_data = {
                "query": "test query",
                "limit": 5
            }
            async with session.post(
                f"{base_url}/search",
                json=search_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"   ✅ Search: Working")
                    print(f"   📝 Query: {data.get('query', 'N/A')}")
                    print(f"   📊 Results: {data.get('total_results', 0)}")
                    print(f"   ⚡ Time: {data.get('processing_time', 'N/A')}s")
                else:
                    print(f"   ❌ Search failed: {response.status}")
        except Exception as e:
            print(f"   ❌ Search error: {e}")
    
    print(f"""
🎯 Test Summary
===============
• Basic connectivity test completed
• Check individual results above
• All green ✅ means everything is working!

🔗 Quick Links:
• Dashboard: {base_url}/
• API Docs: {base_url}/docs
• Health: {base_url}/health
• Database: {base_url}/health/database

💡 Next Steps:
• Upload some documents via the frontend
• Try searching for content
• Monitor the analytics dashboard
""")

async def main():
    """Main test function"""
    await test_api()

if __name__ == "__main__":
    asyncio.run(main())
