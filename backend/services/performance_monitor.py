# backend/services/performance_monitor.py
import time
from datetime import datetime

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {}
        
    async def start_tracking(self, document_id: str):
        self.metrics[document_id] = {
            "start_time": time.time(),
            "document_size": 0,
            "processing_stages": []
        }
        
    async def track_stage(self, document_id: str, stage_name: str):
        if document_id in self.metrics:
            self.metrics[document_id]["processing_stages"].append({
                "stage": stage_name,
                "time": time.time() - self.metrics[document_id]["start_time"]
            })
            
    async def complete_tracking(self, document_id: str):
        if document_id in self.metrics:
            total_time = time.time() - self.metrics[document_id]["start_time"]
            # Check if meeting 5-second benchmark for 5 pages
            if total_time > 5:
                print(f"Performance warning: Processing exceeded benchmark time")
            return total_time