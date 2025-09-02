#!/usr/bin/env python3
"""
Test script for Phase 3 AI Features
Tests document summarization, question answering, and content analysis
"""

import asyncio
import httpx
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

async def test_document_summarization():
    """Test the AI document summarization endpoint"""
    print("\n🤖 Testing Document Summarization...")
    
    async with httpx.AsyncClient() as client:
        # Test with sample text
        test_text = """
        Artificial Intelligence (AI) has revolutionized many industries in recent years. 
        Machine learning algorithms can now process vast amounts of data to identify patterns 
        and make predictions with remarkable accuracy. Deep learning, a subset of machine learning, 
        uses neural networks with multiple layers to solve complex problems. Natural language 
        processing allows computers to understand and generate human language. Computer vision 
        enables machines to interpret and analyze visual information. These technologies are 
        being applied in healthcare for medical diagnosis, in finance for fraud detection, 
        in transportation for autonomous vehicles, and in many other fields. The potential 
        for AI to transform society is immense, but it also raises important ethical considerations 
        about privacy, employment, and decision-making transparency.
        """
        
        payload = {
            "text": test_text,
            "max_length": 100,
            "summary_type": "standard"
        }
        
        try:
            response = await client.post(f"{BASE_URL}/ai/summarize", json=payload)
            if response.status_code == 200:
                result = response.json()
                print("✅ Document Summarization successful!")
                print(f"📄 Original length: {result['original_length']} words")
                print(f"📝 Summary length: {result['summary_length']} words")
                print(f"🔗 Compression ratio: {result['compression_ratio']:.2f}")
                print(f"📋 Summary: {result['summary']}")
                print(f"🔑 Key points: {', '.join(result['key_points'])}")
                return True
            else:
                print(f"❌ Summarization failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error testing summarization: {e}")
            return False

async def test_question_answering():
    """Test the AI question answering endpoint"""
    print("\n❓ Testing Question Answering...")
    
    async with httpx.AsyncClient() as client:
        payload = {
            "question": "What is artificial intelligence?",
            "context_limit": 3,
            "confidence_threshold": 0.3
        }
        
        try:
            response = await client.post(f"{BASE_URL}/ai/question", json=payload)
            if response.status_code == 200:
                result = response.json()
                print("✅ Question Answering successful!")
                print(f"❓ Question: {result['question']}")
                print(f"💬 Answer: {result['answer']}")
                print(f"🎯 Confidence: {result['confidence']:.2f}")
                print(f"⏱️ Processing time: {result['processing_time']:.2f}s")
                return True
            else:
                print(f"❌ Question answering failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error testing question answering: {e}")
            return False

async def test_content_analysis():
    """Test the AI content analysis endpoint"""
    print("\n🔍 Testing Content Analysis...")
    
    async with httpx.AsyncClient() as client:
        test_text = """
        The quarterly financial report shows impressive growth across all sectors. 
        Revenue increased by 15% compared to the previous quarter, with particularly 
        strong performance in the technology and healthcare divisions. The company's 
        innovative products and strategic partnerships have contributed to this success. 
        Our customers have expressed high satisfaction with our services, and employee 
        morale remains positive. Looking ahead, we anticipate continued growth in the 
        coming quarters, driven by new product launches and market expansion initiatives.
        """
        
        payload = {
            "text": test_text,
            "analysis_types": ["classification", "entities", "sentiment"]
        }
        
        try:
            response = await client.post(f"{BASE_URL}/ai/analyze", json=payload)
            if response.status_code == 200:
                result = response.json()
                print("✅ Content Analysis successful!")
                print(f"📊 Document type: {result['document_type']}")
                print(f"🎯 Confidence: {result['confidence']:.2f}")
                print(f"🌍 Language: {result['language']}")
                print(f"📈 Complexity score: {result['complexity_score']:.2f}")
                print(f"😊 Sentiment: {result['sentiment']}")
                print(f"🏷️ Entities found: {len(result['entities'])}")
                print(f"⏱️ Processing time: {result['processing_time']:.2f}s")
                return True
            else:
                print(f"❌ Content analysis failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error testing content analysis: {e}")
            return False

async def test_health_endpoint():
    """Test the health endpoint to ensure services are running"""
    print("\n🏥 Testing Health Endpoint...")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                result = response.json()
                print("✅ Health check successful!")
                print(f"📊 Status: {result['status']}")
                print(f"⏰ Timestamp: {result['timestamp']}")
                print("🔧 Services:")
                for service, status in result['services'].items():
                    print(f"   • {service}: {status}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error testing health endpoint: {e}")
            return False

async def test_root_endpoint():
    """Test the root endpoint to see Phase 3 capabilities"""
    print("\n🏠 Testing Root Endpoint...")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/")
            if response.status_code == 200:
                result = response.json()
                print("✅ Root endpoint successful!")
                print(f"🏷️ Name: {result['name']}")
                print(f"📝 Description: {result['description']}")
                print(f"🔧 Available endpoints:")
                for endpoint, path in result['endpoints'].items():
                    print(f"   • {endpoint}: {path}")
                return True
            else:
                print(f"❌ Root endpoint failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error testing root endpoint: {e}")
            return False

async def main():
    """Run all Phase 3 AI tests"""
    print("🚀 ConfluxAI Phase 3 AI Features Test Suite")
    print("=" * 50)
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    
    # Test all endpoints
    results.append(await test_root_endpoint())
    results.append(await test_health_endpoint())
    results.append(await test_document_summarization())
    results.append(await test_question_answering())
    results.append(await test_content_analysis())
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    passed = sum(results)
    total = len(results)
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 All Phase 3 AI features are working correctly!")
    else:
        print("⚠️ Some tests failed. Check the logs above for details.")
    
    print(f"⏰ Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    asyncio.run(main())
