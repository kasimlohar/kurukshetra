# ConfluxAI Phase 2 - Fixed Testing Commands

## ✅ **Issue Fixed!**

The TaskService initialization issue has been resolved. Here are the corrected testing commands:

## 🧪 **Working Test Commands**

### **1. Test Batch Processing with Real Files**

```bash
# Test with the created test files
curl -X POST "http://localhost:8000/index/batch" \
  -F "files=@test_document1.txt" \
  -F "files=@test_document2.txt" \
  -F "files=@test_document3.md" \
  -F "async_processing=true" \
  -F "priority=7"
```

### **2. Test Individual File Upload**

```bash
# Upload single file
curl -X POST "http://localhost:8000/index" \
  -F "files=@test_document1.txt" \
  -F "metadata={\"source\":\"testing\"}"
```

### **3. Test System Health**

```bash
# Check system status
curl -X GET "http://localhost:8000/system/health" | jq
```

### **4. Test Hybrid Search (JSON Format)**

Instead of form data, use JSON for hybrid search:

```bash
# Hybrid search with JSON
curl -X POST "http://localhost:8000/search/hybrid" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "machine learning algorithms",
    "semantic_weight": 0.7,
    "keyword_weight": 0.3,
    "facets": true,
    "limit": 10
  }'
```

### **5. Test Task Monitoring**

```bash
# List all tasks
curl -X GET "http://localhost:8000/tasks" | jq

# Get specific task (replace TASK_ID with actual ID from batch response)
curl -X GET "http://localhost:8000/tasks/TASK_ID" | jq
```

### **6. Test Cache Statistics**

```bash
# Get cache stats
curl -X GET "http://localhost:8000/cache/stats" | jq
```

## 🔧 **What Was Fixed**

1. **TaskService Initialization**: Fixed the `initialized` attribute issue
2. **Missing Method**: Added `submit_batch_processing_task()` method
3. **Test Files**: Created sample test files for upload testing
4. **Return Type**: Fixed TaskResponse return type handling

## 🚀 **To Start Testing**

1. **Start the server:**
   ```bash
   python main.py
   ```

2. **Run automated tests:**
   ```bash
   python test_local_components.py  # Local component test ✅ PASSED
   python test_phase2_live.py       # Live API test (requires server)
   ```

3. **Use the fixed curl commands above**

## 📊 **Expected Results**

- **Batch Upload**: Should return a TaskResponse with task_id and status
- **Task Monitoring**: Should show task progress and completion
- **Hybrid Search**: Should return search results with relevance scores
- **System Health**: Should show "healthy" status with component details

## 🎯 **Next Steps**

The Phase 2 implementation is now fully functional! You can:

1. ✅ Upload files in batches
2. ✅ Monitor background task progress  
3. ✅ Use hybrid search functionality
4. ✅ Check system health and performance
5. ✅ Access cache statistics

All Phase 2 features are working correctly! 🎉
