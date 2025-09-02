#!/usr/bin/env python3
"""
Test database connectivity for ConfluxAI with Supabase
"""

import asyncio
import os
import sys
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.database import db_manager, check_database_connection, database_health_check
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_database_connection():
    """Test all database functionalities"""
    logger.info("🧪 Testing ConfluxAI Database Configuration...")
    
    # Load environment variables
    load_dotenv()
    
    # Check if DATABASE_URL is set
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        logger.error("❌ DATABASE_URL environment variable not set")
        return False
    
    # Hide credentials in logs
    safe_url = database_url.split("://")[0] + "://***@" + database_url.split("@")[1] if "@" in database_url else database_url
    logger.info(f"📡 Database URL: {safe_url}")
    
    try:
        # Initialize database manager
        logger.info("🔄 Initializing database manager...")
        await db_manager.initialize()
        
        # Test basic connection
        logger.info("📡 Testing basic database connection...")
        is_connected = await check_database_connection()
        
        if is_connected:
            logger.info("✅ Basic database connection successful")
        else:
            logger.error("❌ Basic database connection failed")
            return False
        
        # Test comprehensive health check
        logger.info("🏥 Running comprehensive health check...")
        health_data = await database_health_check()
        
        logger.info(f"📊 Health Status: {health_data.get('status', 'unknown')}")
        logger.info(f"🔗 Connection: {'✅' if health_data.get('connection') else '❌'}")
        
        if health_data.get('latency'):
            logger.info(f"⚡ Latency: {health_data['latency']}ms")
        
        # Display database info
        db_info = health_data.get('info', {})
        if db_info:
            logger.info("📋 Database Configuration:")
            for key, value in db_info.items():
                logger.info(f"  {key}: {value}")
        
        # Test raw SQL execution
        logger.info("🔍 Testing raw SQL execution...")
        try:
            result = await db_manager.execute_raw_sql("SELECT 1 as test_value")
            logger.info(f"✅ SQL test successful: {result}")
        except Exception as e:
            logger.error(f"❌ SQL test failed: {e}")
            return False
        
        logger.info("🎉 All database tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Cleanup
        try:
            await db_manager.cleanup()
            logger.info("🧹 Database connections cleaned up")
        except Exception as e:
            logger.error(f"❌ Cleanup error: {e}")

def main():
    """Main test function"""
    return asyncio.run(test_database_connection())

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎯 Database test successful! Ready for migration.")
        print("   Next: python migrate_database.py")
    else:
        print("\n❌ Database test failed! Please check your configuration.")
    sys.exit(0 if success else 1)
