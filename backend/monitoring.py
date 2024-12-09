# backend/monitoring.py
import time
from datetime import datetime

class PerformanceMonitor:
    def __init__(self):
        self.processing_times = []
        
    def track_processing_time(self, start_time: float, document_size: int):
        processing_time = time.time() - start_time
        self.processing_times.append({
            'time': processing_time,
            'size': document_size,
            'timestamp': datetime.now()
        })
        
        # Check if meeting performance benchmark (5 seconds for 5 pages)
        if processing_time > 5 and document_size <= 5:
            print(f"Performance warning: Processing took {processing_time} seconds")
        
        return processing_time