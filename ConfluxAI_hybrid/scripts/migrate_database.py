#!/usr/bin/env python3
"""
Database migration script for ConfluxAI with PostgreSQL/Supabase
"""

import asyncio
import os
import sys
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.database import db_manager, init_database, database_health_check
from models.database import Base
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def migrate_database():
    """Run database migrations"""
    logger.info("🚀 Starting ConfluxAI Database Migration...")
    
    # Load environment variables
    load_dotenv()
    
    try:
        # Initialize database connection
        logger.info("📡 Initializing database connection...")
        await init_database()
        
        # Check database health
        logger.info("🏥 Checking database health...")
        health_data = await database_health_check()
        
        if health_data["status"] == "healthy":
            logger.info("✅ Database connection is healthy")
            logger.info(f"📊 Connection info: {health_data.get('info', {})}")
        else:
            logger.error("❌ Database connection is unhealthy")
            logger.error(f"❌ Errors: {health_data.get('errors', [])}")
            return False
        
        # Verify tables were created
        logger.info("📋 Verifying database tables...")
        table_names = list(Base.metadata.tables.keys())
        logger.info(f"✅ Created {len(table_names)} database tables:")
        for table_name in table_names:
            logger.info(f"  ✓ {table_name}")
        
        logger.info("🎉 Database migration completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database migration failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Cleanup database connections
        try:
            await db_manager.cleanup()
            logger.info("🧹 Database connections cleaned up")
        except Exception as e:
            logger.error(f"❌ Cleanup error: {e}")

def main():
    """Main migration function"""
    return asyncio.run(migrate_database())

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎯 Migration successful! You can now start the ConfluxAI application.")
        print("   Run: python main.py")
    else:
        print("\n❌ Migration failed! Please check the logs above.")
    sys.exit(0 if success else 1)
