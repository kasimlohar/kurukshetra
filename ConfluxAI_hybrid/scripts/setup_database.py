"""
Database migration script for ConfluxAI with PostgreSQL/Supabase
"""

import asyncio
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.database import db_manager, init_database, check_database_connection
from models.database import Base
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def run_migration():
    """Run database migration"""
    logger.info("🔄 Starting ConfluxAI database migration...")
    
    try:
        # Load environment variables
        load_dotenv()
        
        # Check if DATABASE_URL is set
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            logger.error("❌ DATABASE_URL environment variable not set")
            return False
        
        logger.info(f"📡 Connecting to database: {database_url.split('://')[0]}://***")
        
        # Initialize database
        await init_database()
        
        # Verify connection
        is_connected = await check_database_connection()
        if not is_connected:
            logger.error("❌ Database connection failed")
            return False
        
        logger.info("✅ Database migration completed successfully")
        
        # List created tables
        logger.info("📋 Database tables created:")
        for table_name in Base.metadata.tables.keys():
            logger.info(f"  ✅ {table_name}")
        
        # Get database info
        db_info = await db_manager.get_database_info()
        logger.info("ℹ️ Database configuration:")
        for key, value in db_info.items():
            logger.info(f"  {key}: {value}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Database migration failed: {e}")
        return False

def main():
    """Main migration function"""
    success = asyncio.run(run_migration())
    if success:
        logger.info("🎉 Migration completed successfully!")
        sys.exit(0)
    else:
        logger.error("💥 Migration failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
