#!/usr/bin/env python3
"""
Simple PostgreSQL connection test
"""

import asyncio
import asyncpg
import os
from dotenv import load_dotenv

async def test_simple_connection():
    """Test simple asyncpg connection"""
    load_dotenv()
    
    # Get database URL
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ No DATABASE_URL found")
        return False
    
    # Convert to asyncpg format (remove +asyncpg)
    asyncpg_url = database_url.replace("postgresql+asyncpg://", "postgresql://")
    
    print(f"🔗 Testing connection to: {asyncpg_url.split('@')[1] if '@' in asyncpg_url else 'localhost'}")
    
    try:
        # Try direct asyncpg connection
        conn = await asyncpg.connect(asyncpg_url)
        print("✅ Connection successful!")
        
        # Test simple query
        result = await conn.fetchval("SELECT 1")
        print(f"✅ Query test successful: {result}")
        
        # Get version
        version = await conn.fetchval("SELECT version()")
        print(f"📊 PostgreSQL version: {version[:50]}...")
        
        await conn.close()
        print("✅ Connection closed successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_simple_connection())
    print(f"\n{'🎉 Success!' if success else '❌ Failed!'}")
