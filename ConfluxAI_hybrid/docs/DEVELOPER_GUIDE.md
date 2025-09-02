# ConfluxAI - Developer Quick Reference

## 🚀 **Quick Commands**

### **Start Development**
```bash
# Clone and setup
cd "d:\Kurushetra hackathon\kurukshetra\ConfluxAI_hybrid"
python setup.py                    # Install dependencies
python main.py                     # Start server
```

### **Development Workflow**
```bash
python test_api.py                 # Test API endpoints
python -m pytest tests/           # Run unit tests
black .                           # Format code
flake8 .                         # Check code quality
```

### **API Testing**
```bash
# Health check
curl http://localhost:8000/health

# Index a file
curl -X POST "http://localhost:8000/index" -F "files=@document.pdf"

# Search
curl -X POST "http://localhost:8000/search" -F "query=machine learning"

# Get stats
curl http://localhost:8000/index/stats
```

## 📋 **Development Checklist**

### **Phase 2 Priorities**
- [ ] Enhanced PDF processing with table extraction
- [ ] Improved image analysis (object detection)
- [ ] PowerPoint and HTML file support
- [ ] Hybrid search (semantic + keyword)
- [ ] Search filters and facets
- [ ] Async background processing
- [ ] Redis caching layer
- [ ] Basic React frontend

### **Code Quality Standards**
- [ ] Type hints for all functions
- [ ] Unit tests for new features
- [ ] Error handling and logging
- [ ] API documentation updates
- [ ] Performance benchmarks

## 🛠️ **Key Files to Modify**

### **Adding New File Types**
1. `utils/file_processor.py` - Add new processor method
2. `config/settings.py` - Update ALLOWED_EXTENSIONS
3. `tests/` - Add tests for new format

### **Enhancing Search**
1. `services/search_service.py` - Core search logic
2. `main.py` - API endpoints
3. `models/schemas.py` - Request/response models

### **Performance Improvements**
1. `services/indexing_service.py` - Background processing
2. `config/settings.py` - Cache and performance settings
3. `main.py` - Async endpoints

## 🎯 **Next Implementation Steps**

### **Week 1: Enhanced PDF Processing**
```python
# Install additional libraries
pip install pdfplumber tabula-py

# Implement in utils/file_processor.py
async def _process_pdf_advanced(self, file_path: str):
    # Add table extraction
    # Add image extraction
    # Improve text layout preservation
```

### **Week 2: Image Analysis**
```python
# Install computer vision
pip install opencv-python transformers

# Enhance _process_image method
async def _process_image_advanced(self, file_path: str):
    # Add object detection
    # Improve OCR confidence
    # Add image classification
```

### **Week 3: Hybrid Search**
```python
# Install BM25 for keyword search
pip install rank-bm25

# Create hybrid search service
class HybridSearchService:
    def combine_results(self, semantic_results, keyword_results):
        # Implement result fusion
```

## 📊 **Performance Targets**

```python
# Phase 2 Goals
SEARCH_RESPONSE_TIME = 500      # milliseconds
FILE_PROCESSING_TIME = 5000     # milliseconds per MB
CONCURRENT_USERS = 100          # simultaneous users
SUPPORTED_FORMATS = 15          # file formats
SEARCH_ACCURACY = 0.90          # precision@10
```

## 🔧 **Environment Setup**

### **Development Environment**
```bash
# Python 3.8+
python --version

# Required tools
pip install black flake8 pytest
pip install -r requirements.txt

# Optional (for advanced features)
pip install redis celery
pip install opencv-python transformers
```

### **Production Environment**
```bash
# Production dependencies
pip install gunicorn
pip install redis
pip install postgresql-adapter

# Environment variables
export ENVIRONMENT=production
export DATABASE_URL=postgresql://...
export REDIS_URL=redis://...
```

## 🐛 **Common Issues & Solutions**

### **Installation Issues**
```bash
# Python 3.13 compatibility
python -m pip install --upgrade pip setuptools wheel
python -m pip install "numpy>=1.26.0"

# Tesseract OCR missing
# Windows: choco install tesseract
# Ubuntu: sudo apt-get install tesseract-ocr
# macOS: brew install tesseract
```

### **Performance Issues**
```python
# Reduce chunk size for memory
CHUNK_SIZE = 256  # instead of 512

# Use CPU-optimized FAISS
pip install faiss-cpu  # instead of faiss-gpu

# Enable async processing
USE_ASYNC_PROCESSING = True
```

## 📈 **Monitoring & Metrics**

### **Key Metrics to Track**
```python
# Performance metrics
- Search response time
- File processing time
- Memory usage
- CPU utilization
- Error rates

# Business metrics
- Number of indexed files
- Search queries per day
- User adoption
- Feature usage
```

### **Health Check Endpoints**
```bash
GET /health                     # Overall system health
GET /index/stats               # Indexing statistics
GET /metrics                   # Performance metrics (to implement)
```

## 🚀 **Deployment Guide**

### **Local Development**
```bash
python main.py                 # Development server
# Access: http://localhost:8000
```

### **Production Deployment**
```bash
# Using Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

# Using Docker (to implement)
docker build -t conflux-ai .
docker run -p 8000:8000 conflux-ai

# Using Kubernetes (to implement)
kubectl apply -f k8s/
```

---

**Quick Links:**
- 📋 [Full Roadmap](ROADMAP.md)
- 📖 [API Docs](http://localhost:8000/docs)
- 🧪 [Test Script](test_api.py)
