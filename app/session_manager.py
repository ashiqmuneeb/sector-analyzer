from typing import Dict
import time
from fastapi import Request
import logging

logger = logging.getLogger(__name__)

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, dict] = {}
        
    def create_session(self, request: Request) -> str:
        """Create a new session for the user"""
        session_id = str(hash(request.client.host + str(time.time())))
        self.sessions[session_id] = {
            "ip": request.client.host,
            "created_at": time.time(),
            "last_activity": time.time(),
            "request_count": 0
        }
        logger.info(f"New session created: {session_id}")
        return session_id
        
    def update_session(self, session_id: str):
        """Update session activity"""
        if session_id in self.sessions:
            self.sessions[session_id]["last_activity"] = time.time()
            self.sessions[session_id]["request_count"] += 1
            logger.debug(f"Session updated: {session_id}")
            
    def get_session(self, session_id: str) -> dict:
        """Get session data"""
        return self.sessions.get(session_id, {})

session_manager = SessionManager()