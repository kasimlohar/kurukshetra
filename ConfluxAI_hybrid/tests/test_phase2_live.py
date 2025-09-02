#!/usr/bin/env python3
"""
Test script for ConfluxAI Phase 2 batch processing functionality
"""

import asyncio
import aiohttp
import json
import os
from pathlib import Path

async def test_batch_processing():
    """Test the batch processing endpoint"""
    
    print("🧪 Testing ConfluxAI Phase 2 Batch Processing")
    print("=" * 50)
    
    # Check if server is running
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:8000/system/health") as resp:
                if resp.status == 200:
                    health = await resp.json()
                    print(f"✅ Server is running - Status: {health.get('status', 'unknown')}")
                else:
                    print("❌ Server is not responding properly")
                    return
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("Please start the server with: python main.py")
        return
    
    # Test files to upload
    test_files = [
        "test_document1.txt",
        "test_document2.txt", 
        "test_document3.md"
    ]
    
    # Check if test files exist
    missing_files = []
    for file in test_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing test files: {missing_files}")
        return
    
    print(f"📁 Found {len(test_files)} test files")
    
    # Test batch upload
    try:
        async with aiohttp.ClientSession() as session:
            # Prepare multipart form data
            data = aiohttp.FormData()
            
            # Add files
            for file_path in test_files:
                with open(file_path, 'rb') as f:
                    data.add_field('files', f, filename=os.path.basename(file_path))
            
            # Add form parameters
            data.add_field('async_processing', 'true')
            data.add_field('priority', '7')
            data.add_field('metadata', json.dumps({
                "test_batch": True,
                "source": "phase2_testing"
            }))
            
            print("📤 Uploading files for batch processing...")
            
            async with session.post("http://localhost:8000/index/batch", data=data) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    print(f"✅ Batch upload successful!")
                    print(f"   Task ID: {result.get('task_id')}")
                    print(f"   Status: {result.get('status')}")
                    print(f"   Message: {result.get('message')}")
                    
                    # Monitor task progress
                    task_id = result.get('task_id')
                    if task_id:
                        await monitor_task(session, task_id)
                        
                else:
                    error_text = await resp.text()
                    print(f"❌ Batch upload failed: {resp.status}")
                    print(f"   Error: {error_text}")
                    
    except Exception as e:
        print(f"❌ Batch processing test failed: {e}")

async def monitor_task(session, task_id):
    """Monitor task progress"""
    print(f"\n📊 Monitoring task {task_id}...")
    
    for i in range(10):  # Check up to 10 times
        try:
            async with session.get(f"http://localhost:8000/tasks/{task_id}") as resp:
                if resp.status == 200:
                    task = await resp.json()
                    status = task.get('status')
                    progress = task.get('progress', 0)
                    message = task.get('message', 'No message')
                    
                    print(f"   Status: {status} ({progress:.1f}%) - {message}")
                    
                    if status in ['success', 'failed', 'cancelled']:
                        if status == 'success':
                            result = task.get('result', {})
                            indexed = result.get('total_processed', 0)
                            failed = result.get('total_failed', 0)
                            print(f"✅ Task completed: {indexed} files indexed, {failed} failed")
                        else:
                            error = task.get('error', 'Unknown error')
                            print(f"❌ Task failed: {error}")
                        break
                else:
                    print(f"❌ Failed to get task status: {resp.status}")
                    break
                    
        except Exception as e:
            print(f"❌ Error monitoring task: {e}")
            break
            
        await asyncio.sleep(1)  # Wait 1 second between checks

async def test_hybrid_search():
    """Test hybrid search functionality"""
    print(f"\n🔍 Testing Hybrid Search...")
    
    try:
        async with aiohttp.ClientSession() as session:
            # Prepare search data
            data = aiohttp.FormData()
            data.add_field('query', 'machine learning algorithms')
            data.add_field('semantic_weight', '0.7')
            data.add_field('keyword_weight', '0.3')
            data.add_field('facets', 'true')
            data.add_field('limit', '10')
            
            async with session.post("http://localhost:8000/search/hybrid", data=data) as resp:
                if resp.status == 200:
                    results = await resp.json()
                    print(f"✅ Hybrid search successful!")
                    print(f"   Found {len(results.get('results', []))} results")
                    
                    # Show first result if available
                    if results.get('results'):
                        first_result = results['results'][0]
                        print(f"   Top result: {first_result.get('filename', 'Unknown')}")
                        print(f"   Score: {first_result.get('score', 0):.3f}")
                else:
                    error_text = await resp.text()
                    print(f"❌ Hybrid search failed: {resp.status}")
                    print(f"   Error: {error_text}")
                    
    except Exception as e:
        print(f"❌ Hybrid search test failed: {e}")

async def main():
    """Run all tests"""
    await test_batch_processing()
    await test_hybrid_search()
    
    print("\n🎉 Phase 2 Testing Complete!")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
