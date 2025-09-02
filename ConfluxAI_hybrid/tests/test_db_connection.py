"""
Simple database connection test
"""

import asyncio
import asyncpg
import os
from dotenv import load_dotenv

async def test_connection():
    """Test basic database connection"""
    load_dotenv()
    
    # Get database URL
    database_url = os.getenv("DATABASE_URL")
    print(f"Testing connection to: {database_url.split('://')[0]}://***")
    
    # Parse URL for asyncpg
    # Remove the +asyncpg part and use asyncpg.connect directly
    asyncpg_url = database_url.replace("postgresql+asyncpg://", "postgresql://")
    
    try:
        # Try to connect
        print("Attempting connection...")
        conn = await asyncpg.connect(asyncpg_url)
        
        # Test query
        result = await conn.fetchval("SELECT version()")
        print(f"✅ Connection successful!")
        print(f"PostgreSQL version: {result}")
        
        # Close connection
        await conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_connection())
    if success:
        print("🎉 Database connection test passed!")
    else:
        print("💥 Database connection test failed!")
