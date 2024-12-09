# backend/services/status_tracker.py
class StatusTracker:
    def __init__(self):
        self.processing_status = {}
        
    async def update_status(self, document_id: str, status: dict):
        self.processing_status[document_id] = {
            "status": status["state"],
            "progress": status["progress"],
            "estimated_time": status["estimated_time"]
        }
        
    async def get_status(self, document_id: str):
        return self.processing_status.get(document_id, {
            "status": "not_found",
            "progress": 0,
            "estimated_time": 0
        })