"""
Test script to verify the hybrid search fix
"""
import aiohttp
import asyncio
import json

async def test_hybrid_search():
    """Test the fixed hybrid search endpoint"""
    
    print("🔍 Testing fixed hybrid search endpoint...")
    
    async with aiohttp.ClientSession() as session:
        # Test data
        data = aiohttp.FormData()
        data.add_field('query', 'machine learning algorithms')
        data.add_field('semantic_weight', '0.7')
        data.add_field('keyword_weight', '0.3')
        data.add_field('facets', 'true')
        data.add_field('limit', '10')
        
        try:
            async with session.post("http://localhost:8000/search/hybrid", data=data) as response:
                print(f"Status: {response.status}")
                
                if response.status == 200:
                    result = await response.json()
                    print("✅ Hybrid search successful!")
                    print(f"Query: {result.get('query', 'N/A')}")
                    print(f"Results: {len(result.get('results', []))}")
                    print(f"Search type: {result.get('search_type', 'N/A')}")
                    print(f"Processing time: {result.get('processing_time', 0):.3f}s")
                    
                    if result.get('facets'):
                        print("✅ Facets included")
                    
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ Hybrid search failed: {response.status}")
                    print(f"Error: {error_text}")
                    return False
                    
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False

async def test_hybrid_search_with_filters():
    """Test hybrid search with filters"""
    
    print("\n🔍 Testing hybrid search with filters...")
    
    async with aiohttp.ClientSession() as session:
        # Test data with filters
        data = aiohttp.FormData()
        data.add_field('query', 'data analysis')
        data.add_field('file_types', 'pdf')
        data.add_field('file_types', 'docx')
        data.add_field('sort_by', 'relevance')
        data.add_field('facets', 'true')
        
        try:
            async with session.post("http://localhost:8000/search/hybrid", data=data) as response:
                print(f"Status: {response.status}")
                
                if response.status == 200:
                    result = await response.json()
                    print("✅ Hybrid search with filters successful!")
                    print(f"Query: {result.get('query', 'N/A')}")
                    print(f"Results: {len(result.get('results', []))}")
                    print(f"Search type: {result.get('search_type', 'N/A')}")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ Hybrid search with filters failed: {response.status}")
                    print(f"Error: {error_text}")
                    return False
                    
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False

async def main():
    """Run all tests"""
    print("🧪 Testing ConfluxAI Hybrid Search Fix")
    print("=" * 50)
    
    test1 = await test_hybrid_search()
    test2 = await test_hybrid_search_with_filters()
    
    print("\n" + "=" * 50)
    if test1 and test2:
        print("🎉 All hybrid search tests PASSED!")
        print("✅ The File object error has been fixed!")
    else:
        print("❌ Some tests failed")
    
    return test1 and test2

if __name__ == "__main__":
    success = asyncio.run(main())
