"""
Development server for ConfluxAI
Quick start for development with hot reload
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start_dev_server():
    """Start development server"""
    
    # Load environment
    load_dotenv()
    
    print("""
🔥 ConfluxAI Development Server
===============================
    """)
    
    # Check if .env exists
    if not os.path.exists('.env'):
        logger.error("❌ .env file not found!")
        logger.info("💡 Please create .env file first")
        return False
    
    # Get configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    logger.info(f"🖥️  Host: {host}")
    logger.info(f"🔌 Port: {port}")
    logger.info(f"🐛 Debug: {debug}")
    logger.info(f"📡 Backend: http://localhost:{port}")
    logger.info(f"📚 Docs: http://localhost:{port}/docs")
    
    try:
        # Start with uvicorn
        cmd = [
            sys.executable, "-m", "uvicorn",
            "main:app",
            "--host", host,
            "--port", str(port),
            "--reload",
            "--log-level", "info"
        ]
        
        logger.info("🚀 Starting development server...")
        logger.info("💡 Press Ctrl+C to stop")
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        logger.info("🛑 Development server stopped")
    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    start_dev_server()
