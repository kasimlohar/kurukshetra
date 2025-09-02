#!/usr/bin/env python3
"""
ConfluxAI Phase 2 - Quick Start Deployment Script
Starts the ConfluxAI application with all Phase 2 features enabled
"""

import uvicorn
import os
import sys
from pathlib import Path

def main():
    """Start ConfluxAI Phase 2 application"""
    
    print("🚀 ConfluxAI Phase 2 - Multi-Modal Search Agent")
    print("=" * 55)
    print()
    
    # Validate Phase 2 implementation
    print("🔍 Validating Phase 2 implementation...")
    try:
        from services.hybrid_search_service import HybridSearchService
        from services.cache_service import CacheService
        from services.task_service import TaskService
        from models.schemas import HybridSearchRequest, TaskResponse
        print("✅ All Phase 2 services validated")
    except ImportError as e:
        print(f"❌ Phase 2 validation failed: {e}")
        print("Please ensure all dependencies are installed:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    
    print()
    print("🎯 Phase 2 Features Enabled:")
    print("  • Hybrid Search (Semantic + Keyword)")
    print("  • Advanced File Processing (18+ formats)")
    print("  • Redis Caching (optional)")
    print("  • Background Task Processing (optional)")
    print("  • Enhanced API Endpoints")
    print("  • System Health Monitoring")
    print()
    
    # Configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    print(f"🌐 Starting server at http://{host}:{port}")
    print("📊 API Documentation: http://localhost:8000/docs")
    print("📋 Health Check: http://localhost:8000/system/health")
    print()
    print("⚡ Phase 2 Enhanced Endpoints:")
    print("  POST /search/hybrid - Advanced hybrid search")
    print("  GET  /search/suggestions - Query auto-complete")
    print("  POST /index/batch - Batch file processing")
    print("  GET  /tasks/{id} - Task status monitoring")
    print("  GET  /cache/stats - Cache performance stats")
    print("  GET  /system/health - System health check")
    print("  GET  /system/metrics - Performance metrics")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 55)
    
    # Start the application
    try:
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server startup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
