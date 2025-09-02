"""
ConfluxAI Application Startup Script
Complete setup and launch for PostgreSQL/Supabase
"""

import asyncio
import subprocess
import sys
import os
import time
from pathlib import Path
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ConfluxAILauncher:
    """Complete application launcher"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        os.chdir(self.project_root)
        load_dotenv()
    
    def print_banner(self):
        """Print startup banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ██████╗ ██████╗ ███╗   ██╗███████╗██╗     ██╗   ██╗██╗  ██╗ ║
║  ██╔════╝██╔═══██╗████╗  ██║██╔════╝██║     ██║   ██║╚██╗██╔╝ ║
║  ██║     ██║   ██║██╔██╗ ██║█████╗  ██║     ██║   ██║ ╚███╔╝  ║
║  ██║     ██║   ██║██║╚██╗██║██╔══╝  ██║     ██║   ██║ ██╔██╗  ║
║  ╚██████╗╚██████╔╝██║ ╚████║██║     ███████╗╚██████╔╝██╔╝ ██╗ ║
║   ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ║
║                                                              ║
║            AI-Powered Multi-Modal Search Agent               ║
║                    Phase 3 - Production                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
        print("🚀 Starting ConfluxAI with PostgreSQL/Supabase...")
        print("📅 Startup Time:", time.strftime("%Y-%m-%d %H:%M:%S"))
        print("📂 Project Root:", self.project_root)
        print("="*70)
    
    def check_dependencies(self):
        """Check if all dependencies are installed"""
        logger.info("📦 Checking dependencies...")
        
        required_packages = [
            'fastapi',
            'uvicorn',
            'sqlalchemy',
            'asyncpg',
            'psycopg2-binary',
            'alembic',
            'python-dotenv',
            'sentence-transformers',
            'faiss-cpu',
            'redis'
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
                logger.info(f"  ✅ {package}")
            except ImportError:
                missing_packages.append(package)
                logger.error(f"  ❌ {package}")
        
        if missing_packages:
            logger.error(f"Missing packages: {', '.join(missing_packages)}")
            logger.info("Installing missing packages...")
            
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install"
                ] + missing_packages)
                logger.info("✅ Dependencies installed successfully")
            except subprocess.CalledProcessError as e:
                logger.error(f"❌ Failed to install dependencies: {e}")
                return False
        else:
            logger.info("✅ All dependencies are satisfied")
        
        return True
    
    def validate_environment(self):
        """Validate environment configuration"""
        logger.info("🔍 Validating environment...")
        
        try:
            result = subprocess.run([
                sys.executable, "validate_env.py"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✅ Environment validation passed")
                return True
            else:
                logger.error("❌ Environment validation failed")
                print(result.stdout)
                print(result.stderr)
                return False
        except Exception as e:
            logger.error(f"❌ Environment validation error: {e}")
            return False
    
    def setup_database(self):
        """Setup database schema"""
        logger.info("🗄️  Setting up database...")
        
        try:
            result = subprocess.run([
                sys.executable, "setup_database.py"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✅ Database setup completed")
                print(result.stdout)
                return True
            else:
                logger.error("❌ Database setup failed")
                print(result.stdout)
                print(result.stderr)
                return False
        except Exception as e:
            logger.error(f"❌ Database setup error: {e}")
            return False
    
    def start_backend(self):
        """Start the FastAPI backend"""
        logger.info("🖥️  Starting ConfluxAI backend...")
        
        host = os.getenv("HOST", "0.0.0.0")
        port = int(os.getenv("PORT", "8000"))
        
        logger.info(f"📡 Backend will be available at: http://{host}:{port}")
        logger.info("📚 API Documentation: http://localhost:8000/docs")
        logger.info("🔧 Health Check: http://localhost:8000/health")
        logger.info("🗄️  Database Health: http://localhost:8000/health/database")
        
        try:
            # Import uvicorn here to ensure it's available
            import uvicorn
            
            # Run the application
            uvicorn.run(
                "main:app",
                host=host,
                port=port,
                reload=True,
                log_level="info"
            )
        except KeyboardInterrupt:
            logger.info("🛑 Backend stopped by user")
        except Exception as e:
            logger.error(f"❌ Backend startup failed: {e}")
            return False
    
    def run_health_check(self):
        """Run a comprehensive health check"""
        logger.info("🏥 Running health check...")
        
        try:
            import requests
            time.sleep(2)  # Wait for server to start
            
            # Check main health endpoint
            response = requests.get("http://localhost:8000/health", timeout=10)
            if response.status_code == 200:
                logger.info("✅ Backend health check passed")
            else:
                logger.warning(f"⚠️  Backend health check returned {response.status_code}")
            
            # Check database health
            db_response = requests.get("http://localhost:8000/health/database", timeout=10)
            if db_response.status_code == 200:
                logger.info("✅ Database health check passed")
            else:
                logger.warning(f"⚠️  Database health check returned {db_response.status_code}")
            
            return True
            
        except requests.exceptions.RequestException as e:
            logger.warning(f"⚠️  Health check failed: {e}")
            return False
        except ImportError:
            logger.info("ℹ️  Requests not available, skipping health check")
            return True
    
    def launch(self):
        """Main launch sequence"""
        self.print_banner()
        
        # Step 1: Check dependencies
        if not self.check_dependencies():
            logger.error("💥 Dependency check failed")
            return False
        
        # Step 2: Validate environment
        if not self.validate_environment():
            logger.error("💥 Environment validation failed")
            return False
        
        # Step 3: Setup database
        if not self.setup_database():
            logger.error("💥 Database setup failed")
            return False
        
        logger.info("🎉 Pre-flight checks completed successfully!")
        logger.info("🚀 Launching ConfluxAI...")
        
        # Step 4: Start backend
        self.start_backend()
        
        return True

def main():
    """Main function"""
    launcher = ConfluxAILauncher()
    
    try:
        success = launcher.launch()
        if not success:
            logger.error("💥 Launch failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("🛑 Launch interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"💥 Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
