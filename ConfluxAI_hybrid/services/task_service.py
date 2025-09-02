"""
Task management service for ConfluxAI
Handles background task tracking and status management
"""
import json
import uuid
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict

from models.schemas import TaskResponse, TaskStatus as TaskStatusEnum
from config.settings import Settings

logger = logging.getLogger(__name__)

@dataclass
class TaskInfo:
    """Internal task information"""
    task_id: str
    status: str
    progress: float
    message: Optional[str]
    result: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime
    error: Optional[str] = None

class TaskService:
    """Service for managing background tasks"""
    
    def __init__(self):
        self.settings = Settings()
        self.tasks: Dict[str, TaskInfo] = {}
        self.initialized = True  # Initialize as True since no external dependencies
    
    async def initialize(self):
        """Initialize the task service"""
        try:
            logger.info("Initializing task service...")
            
            # Task service is always available (no external dependencies required)
            self.initialized = True
            logger.info("Task service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize task service: {str(e)}")
            raise
        
    def create_task(self, task_type: str, description: str = "") -> str:
        """Create a new task"""
        task_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        task_info = TaskInfo(
            task_id=task_id,
            status="pending",
            progress=0.0,
            message=description or f"Starting {task_type} task",
            result=None,
            created_at=now,
            updated_at=now
        )
        
        self.tasks[task_id] = task_info
        logger.info(f"Created task {task_id}: {task_type}")
        return task_id
    
    def update_task(
        self, 
        task_id: str, 
        status: Optional[str] = None,
        progress: Optional[float] = None,
        message: Optional[str] = None,
        result: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None
    ) -> bool:
        """Update task status"""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        
        if status:
            task.status = status
        if progress is not None:
            task.progress = max(0.0, min(1.0, progress))
        if message:
            task.message = message
        if result:
            task.result = result
        if error:
            task.error = error
            task.status = "failed"
        
        task.updated_at = datetime.utcnow()
        
        logger.debug(f"Updated task {task_id}: {task.status} ({task.progress:.1%})")
        return True
    
    def get_task(self, task_id: str) -> Optional[TaskResponse]:
        """Get task status"""
        if task_id not in self.tasks:
            return None
        
        task = self.tasks[task_id]
        return TaskResponse(
            task_id=task.task_id,
            status=task.status,
            message=task.message or "No message",
            submitted_at=task.created_at,
            started_at=task.created_at,  # Simplified for now
            completed_at=task.updated_at if task.status in ["success", "failed"] else None,
            progress=task.progress * 100,  # Convert to percentage
            result=task.result,
            error=task.error,
            processing_time=None,  # Can be calculated if needed
            metadata={}
        )
    
    def list_tasks(self, status_filter: Optional[str] = None) -> List[TaskResponse]:
        """List all tasks, optionally filtered by status"""
        tasks = []
        
        for task in self.tasks.values():
            if status_filter is None or task.status == status_filter:
                tasks.append(TaskResponse(
                    task_id=task.task_id,
                    status=task.status,
                    message=task.message or "No message",
                    submitted_at=task.created_at,
                    started_at=task.created_at,
                    completed_at=task.updated_at if task.status in ["success", "failed"] else None,
                    progress=task.progress * 100,
                    result=task.result,
                    error=task.error,
                    processing_time=None,
                    metadata={}
                ))
        
        # Sort by creation time, newest first
        tasks.sort(key=lambda x: x.submitted_at, reverse=True)
        return tasks
    
    async def get_task_status(self, task_id: str) -> Optional[TaskResponse]:
        """Get task status (async wrapper for compatibility)"""
        return self.get_task(task_id)
    
    async def cancel_task(self, task_id: str) -> bool:
        """Cancel a task"""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        if task.status in ["success", "failed", "cancelled"]:
            return False  # Already completed
        
        task.status = "cancelled"
        task.updated_at = datetime.utcnow()
        task.message = "Task cancelled by user"
        
        logger.info(f"Cancelled task {task_id}")
        return True
    
    async def get_active_tasks(self) -> List[TaskResponse]:
        """Get all active tasks"""
        return self.list_tasks(status_filter="running")
    
    async def health_check(self) -> Dict[str, Any]:
        """Check service health"""
        total_tasks = len(self.tasks)
        active_tasks = len([t for t in self.tasks.values() if t.status == "running"])
        
        return {
            "status": "healthy" if self.initialized else "unhealthy",
            "initialized": self.initialized,
            "total_tasks": total_tasks,
            "active_tasks": active_tasks,
            "message": "Task service operational"
        }
    
    def cleanup_completed_tasks(self, max_age_hours: int = 24) -> int:
        """Remove completed tasks older than specified hours"""
        cutoff_time = datetime.utcnow() - timedelta(hours=max_age_hours)
        removed_count = 0
        
        tasks_to_remove = []
        for task_id, task in self.tasks.items():
            if (task.status in ["completed", "failed"] and 
                task.updated_at < cutoff_time):
                tasks_to_remove.append(task_id)
        
        for task_id in tasks_to_remove:
            del self.tasks[task_id]
            removed_count += 1
        
        if removed_count > 0:
            logger.info(f"Cleaned up {removed_count} completed tasks")
        
        return removed_count
    
    async def submit_batch_processing_task(
        self, 
        file_infos: List[Dict[str, Any]], 
        priority: int = 5
    ) -> TaskResponse:
        """Submit a batch processing task"""
        try:
            # Create a new task
            task_id = self.create_task(
                task_type="batch_file_processing",
                description=f"Processing {len(file_infos)} files"
            )
            
            # Update task to running
            self.update_task(task_id, status="running", progress=0.0)
            
            # For now, we'll simulate background processing
            # In a real implementation, this would submit to Celery
            # For testing purposes, we'll process files immediately but track progress
            
            try:
                indexed_files = []
                failed_files = []
                total_files = len(file_infos)
                
                for i, file_info in enumerate(file_infos):
                    try:
                        # Update progress
                        progress = (i + 1) / total_files
                        self.update_task(
                            task_id, 
                            progress=progress,
                            message=f"Processing file {i+1}/{total_files}: {file_info['filename']}"
                        )
                        
                        # Simulate file processing
                        # In real implementation, this would call indexing service
                        result = {
                            'filename': file_info['filename'],
                            'status': 'indexed',
                            'size': 'unknown',
                            'processing_time': 0.5
                        }
                        indexed_files.append(result)
                        
                    except Exception as e:
                        failed_files.append({
                            'filename': file_info['filename'],
                            'error': str(e)
                        })
                
                # Complete the task
                result = {
                    'indexed_files': indexed_files,
                    'failed_files': failed_files,
                    'total_processed': len(indexed_files),
                    'total_failed': len(failed_files)
                }
                
                self.update_task(
                    task_id,
                    status="success",
                    progress=1.0,
                    message=f"Batch processing completed: {len(indexed_files)} success, {len(failed_files)} failed",
                    result=result
                )
                
            except Exception as e:
                self.update_task(
                    task_id,
                    status="failed",
                    error=str(e),
                    message=f"Batch processing failed: {str(e)}"
                )
            
            task_response = self.get_task(task_id)
            if task_response is None:
                raise Exception(f"Failed to retrieve task {task_id}")
            return task_response
            
        except Exception as e:
            logger.error(f"Failed to submit batch processing task: {str(e)}")
            raise Exception(f"Task submission failed: {str(e)}")

# Global task service instance
task_service = TaskService()
