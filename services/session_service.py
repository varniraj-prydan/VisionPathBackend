import os
import uuid
from typing import Dict, List

# In-memory session storage (use Redis in production)
sessions: Dict[str, List[str]] = {}

def create_session() -> str:
    session_id = str(uuid.uuid4())
    sessions[session_id] = []
    return session_id

def add_audio_to_session(session_id: str, audio_path: str):
    if session_id in sessions:
        sessions[session_id].append(audio_path)

def cleanup_session(session_id: str):
    if session_id in sessions:
        for audio_path in sessions[session_id]:
            if os.path.exists(audio_path):
                os.remove(audio_path)
        del sessions[session_id]
        return True
    return False

def get_session_files(session_id: str) -> List[str]:
    return sessions.get(session_id, [])