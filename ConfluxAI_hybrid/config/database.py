"""
Database configuration for ConfluxAI with PostgreSQL/Supabase support
"""

import os
import asyncio
import logging
from typing import AsyncGenerator, Optional
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool, QueuePool
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from models.database import Base
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Database configuration from environment
DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_POOL_SIZE = int(os.getenv("DATABASE_POOL_SIZE", "20"))
DATABASE_MAX_OVERFLOW = int(os.getenv("DATABASE_MAX_OVERFLOW", "30"))
DATABASE_POOL_TIMEOUT = int(os.getenv("DATABASE_POOL_TIMEOUT", "30"))
DATABASE_POOL_RECYCLE = int(os.getenv("DATABASE_POOL_RECYCLE", "3600"))
DATABASE_ECHO = os.getenv("DATABASE_ECHO", "False").lower() == "true"

# Validate database URL
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# Determine if using async database
is_async = any(driver in DATABASE_URL for driver in ["asyncpg", "aiomysql", "aiosqlite"])

class DatabaseManager:
    """Database connection and session management"""
    
    def __init__(self):
        self.engine = None
        self.async_session_maker = None
        self.sync_session_maker = None
        self.is_initialized = False
        
    async def initialize(self):
        """Initialize database connection"""
        try:
            if is_async:
                await self._setup_async_database()
            else:
                self._setup_sync_database()
            
            self.is_initialized = True
            logger.info("✅ Database connection initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize database: {e}")
            raise
    
    async def _setup_async_database(self):
        """Setup async database connection for PostgreSQL"""
        logger.info("🔄 Setting up async PostgreSQL connection...")
        
        # Create async engine with optimized settings for Supabase
        self.engine = create_async_engine(
            DATABASE_URL,
            echo=DATABASE_ECHO,
            future=True,
            pool_size=DATABASE_POOL_SIZE,
            max_overflow=DATABASE_MAX_OVERFLOW,
            pool_timeout=DATABASE_POOL_TIMEOUT,
            pool_recycle=DATABASE_POOL_RECYCLE,
            pool_pre_ping=True,  # Validate connections before use
            pool_reset_on_return='commit',  # Reset connections on return
            # Supabase-specific optimizations
            connect_args={
                "server_settings": {
                    "application_name": "ConfluxAI",
                    "jit": "off",  # Disable JIT for faster cold starts
                },
                "command_timeout": 60,
            }
        )
        
        # Create async session maker
        self.async_session_maker = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=True,
            autocommit=False
        )
        
        logger.info("✅ Async database engine created")
    
    def _setup_sync_database(self):
        """Setup sync database connection (fallback)"""
        logger.info("🔄 Setting up sync database connection...")
        
        # Convert async URL to sync if needed
        sync_url = DATABASE_URL.replace("+asyncpg", "").replace("+aiomysql", "")
        
        self.engine = create_engine(
            sync_url,
            echo=DATABASE_ECHO,
            pool_size=DATABASE_POOL_SIZE,
            max_overflow=DATABASE_MAX_OVERFLOW,
            pool_timeout=DATABASE_POOL_TIMEOUT,
            pool_recycle=DATABASE_POOL_RECYCLE,
            pool_pre_ping=True
        )
        
        self.sync_session_maker = sessionmaker(
            bind=self.engine,
            autoflush=True,
            autocommit=False
        )
        
        logger.info("✅ Sync database engine created")
    
    @asynccontextmanager
    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get async database session with proper error handling"""
        if not self.async_session_maker:
            raise RuntimeError("Async database not initialized")
        
        async with self.async_session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                logger.error(f"Database session error: {e}")
                raise
            finally:
                await session.close()
    
    def get_sync_session(self):
        """Get sync database session"""
        if not self.sync_session_maker:
            raise RuntimeError("Sync database not initialized")
        
        session = self.sync_session_maker()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()
    
    async def create_tables(self):
        """Create all database tables"""
        try:
            if is_async:
                async with self.engine.begin() as conn:
                    # Create extensions if needed (for PostgreSQL)
                    if "postgresql" in DATABASE_URL:
                        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\""))
                        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS \"pg_trgm\""))
                        logger.info("✅ PostgreSQL extensions created")
                    
                    await conn.run_sync(Base.metadata.create_all)
                    logger.info("✅ Database tables created successfully")
            else:
                Base.metadata.create_all(bind=self.engine)
                logger.info("✅ Database tables created successfully")
                
        except Exception as e:
            logger.error(f"❌ Failed to create tables: {e}")
            raise
    
    async def drop_tables(self):
        """Drop all database tables (use with caution!)"""
        try:
            if is_async:
                async with self.engine.begin() as conn:
                    await conn.run_sync(Base.metadata.drop_all)
            else:
                Base.metadata.drop_all(bind=self.engine)
            logger.info("✅ Database tables dropped successfully")
        except Exception as e:
            logger.error(f"❌ Failed to drop tables: {e}")
            raise
    
    async def check_connection(self) -> bool:
        """Check database connectivity"""
        try:
            if is_async:
                async with self.get_async_session() as session:
                    await session.execute(text("SELECT 1"))
            else:
                with next(self.get_sync_session()) as session:
                    session.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"Database connection check failed: {e}")
            return False
    
    async def get_database_info(self) -> dict:
        """Get database connection information"""
        try:
            info = {
                "url": DATABASE_URL.split("://")[0] + "://***",  # Hide credentials
                "pool_size": DATABASE_POOL_SIZE,
                "max_overflow": DATABASE_MAX_OVERFLOW,
                "pool_timeout": DATABASE_POOL_TIMEOUT,
                "pool_recycle": DATABASE_POOL_RECYCLE,
                "is_async": is_async,
                "echo": DATABASE_ECHO,
                "engine_type": str(type(self.engine).__name__) if self.engine else "Not initialized"
            }
            
            # Add connection pool stats if available
            if self.engine and hasattr(self.engine.pool, 'size'):
                info.update({
                    "pool_current_size": self.engine.pool.size(),
                    "pool_checked_out": self.engine.pool.checkedout(),
                    "pool_checked_in": self.engine.pool.checkedin()
                })
            
            return info
        except Exception as e:
            logger.error(f"Error getting database info: {e}")
            return {"error": str(e)}
    
    async def execute_raw_sql(self, sql: str, params: dict = None) -> list:
        """Execute raw SQL query"""
        try:
            if is_async:
                async with self.get_async_session() as session:
                    result = await session.execute(text(sql), params or {})
                    return result.fetchall()
            else:
                with next(self.get_sync_session()) as session:
                    result = session.execute(text(sql), params or {})
                    return result.fetchall()
        except Exception as e:
            logger.error(f"Error executing raw SQL: {e}")
            raise
    
    async def cleanup(self):
        """Cleanup database connections"""
        try:
            if self.engine:
                if is_async:
                    await self.engine.dispose()
                else:
                    self.engine.dispose()
                logger.info("✅ Database connections cleaned up")
        except Exception as e:
            logger.error(f"Error cleaning up database: {e}")

# Global database manager instance
db_manager = DatabaseManager()

# Convenience functions for backward compatibility
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session"""
    async with db_manager.get_async_session() as session:
        yield session

def get_db():
    """Get sync database session"""
    yield from db_manager.get_sync_session()

async def init_database():
    """Initialize database connection and create tables"""
    await db_manager.initialize()
    await db_manager.create_tables()

async def check_database_connection() -> bool:
    """Check database connectivity"""
    return await db_manager.check_connection()

def get_database_info() -> dict:
    """Get database information"""
    return asyncio.run(db_manager.get_database_info())

# Health check function
async def database_health_check() -> dict:
    """Comprehensive database health check"""
    health_data = {
        "status": "unhealthy",
        "connection": False,
        "info": {},
        "latency": None,
        "errors": []
    }
    
    try:
        # Check connection
        import time
        start_time = time.time()
        health_data["connection"] = await check_database_connection()
        health_data["latency"] = round((time.time() - start_time) * 1000, 2)  # ms
        
        # Get database info
        health_data["info"] = await db_manager.get_database_info()
        
        # Set overall status
        if health_data["connection"]:
            health_data["status"] = "healthy"
        
    except Exception as e:
        health_data["errors"].append(str(e))
        logger.error(f"Database health check failed: {e}")
    
    return health_data
