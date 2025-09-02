"""
Startup script for ConfluxAI Multi-Modal Search Agent
"""
import os
import sys
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_requirements():
    """Check if required packages are installed"""
    try:
        import fastapi
        import uvicorn
        import sentence_transformers
        import faiss
        import PyPDF2
        import PIL
        import pandas
        import numpy
        logger.info("All required packages are available")
        return True
    except ImportError as e:
        logger.error(f"Missing required package: {e}")
        return False

def install_requirements():
    """Install requirements"""
    try:
        logger.info("Upgrading pip first...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        logger.info("Installing requirements...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        logger.info("Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install requirements: {e}")
        logger.info("Trying alternative installation method...")
        
        # Try installing packages individually if batch install fails
        try:
            essential_packages = [
                "fastapi>=0.104.1",
                "uvicorn[standard]>=0.24.0",
                "python-multipart>=0.0.6",
                "pydantic>=2.5.0",
                "numpy>=1.26.0",
                "sentence-transformers>=2.2.2",
                "faiss-cpu>=1.7.4",
                "PyPDF2>=3.0.1",
                "Pillow>=10.1.0",
                "pytesseract>=0.3.10",
                "python-docx>=1.1.0",
                "openpyxl>=3.1.2",
                "pandas>=2.1.4",
                "nltk>=3.8.1",
                "python-dotenv>=1.0.0"
            ]
            
            for package in essential_packages:
                logger.info(f"Installing {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            
            logger.info("Essential packages installed successfully")
            return True
        except subprocess.CalledProcessError as e2:
            logger.error(f"Failed to install essential packages: {e2}")
            return False

def setup_directories():
    """Create necessary directories"""
    dirs = ["uploads", "indexes", "logs"]
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
        logger.info(f"Created directory: {dir_name}")

def main():
    """Main startup function"""
    logger.info("Starting ConfluxAI Multi-Modal Search Agent setup...")
    logger.info(f"Python version: {sys.version}")
    
    # Setup directories
    setup_directories()
    
    # Check requirements
    if not check_requirements():
        logger.info("Installing missing requirements...")
        if not install_requirements():
            logger.error("Failed to install requirements. Please install manually.")
            logger.error("Try running these commands manually:")
            logger.error("1. python -m pip install --upgrade pip")
            logger.error("2. python -m pip install --upgrade setuptools wheel")
            logger.error("3. python -m pip install -r requirements.txt")
            logger.error("Or install essential packages individually:")
            logger.error("   python -m pip install 'fastapi>=0.104.1' 'uvicorn[standard]>=0.24.0'")
            return False
    
    logger.info("Setup completed successfully!")
    logger.info("You can now start the server with: python main.py")
    logger.info("Or use: uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
    
    return True

if __name__ == "__main__":
    main()
