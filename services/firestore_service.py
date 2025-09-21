from google.cloud import firestore
import uuid
from datetime import datetime
import os

# Initialize Firestore client with explicit project ID
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
print(f"[FIRESTORE] Project ID from env: {project_id}")

try:
    db = firestore.Client(project=project_id) if project_id else None
    print(f"[FIRESTORE] Client initialized: {db is not None}")
except Exception as e:
    print(f"[FIRESTORE] Client initialization failed: {e}")
    db = None

def save_roadmap(topic, description, roadmap_json, summary=None, summary_audio_path=None):
    roadmap_id = str(uuid.uuid4())
    
    if not db:
        # For demo purposes, return a dummy ID when database is not configured
        print("[FIRESTORE] Database not configured, returning dummy roadmap ID")
        return roadmap_id
    
    try:
        doc_ref = db.collection("roadmaps").document(roadmap_id)
        doc_ref.set({
            "topic": topic,
            "description": description,
            "roadmap": roadmap_json,
            "summary": summary,
            "summary_audio_path": summary_audio_path,
            "created_at": datetime.now()
        })
        print(f"[FIRESTORE] Roadmap saved with ID: {roadmap_id}")
    except Exception as e:
        print(f"[FIRESTORE] Failed to save roadmap, continuing anyway: {e}")
    
    return roadmap_id

def get_lesson(roadmap_id, day):
    if not db:
        raise Exception("Firestore not configured. Check GOOGLE_CLOUD_PROJECT in .env")
    
    doc_ref = db.collection("roadmaps").document(roadmap_id)
    doc = doc_ref.get()
    
    if doc.exists:
        roadmap = doc.to_dict()["roadmap"]
        for day_data in roadmap["days"]:
            if day_data["day"] == day:
                return day_data
    
    return None

def get_all_roadmaps():
    if not db:
        raise Exception("Firestore not configured. Check GOOGLE_CLOUD_PROJECT in .env")
    
    docs = db.collection("roadmaps").stream()
    roadmaps = []
    
    for doc in docs:
        data = doc.to_dict()
        roadmaps.append({
            "id": doc.id,
            "topic": data["topic"],
            "description": data["description"],
            "summary": data.get("summary", ""),
            "created_at": data["created_at"]
        })
    
    return roadmaps

def get_single_roadmap(roadmap_id):
    if not db:
        raise Exception("Firestore not configured. Check GOOGLE_CLOUD_PROJECT in .env")
    
    doc_ref = db.collection("roadmaps").document(roadmap_id)
    doc = doc_ref.get()
    
    if doc.exists:
        data = doc.to_dict()
        return {
            "id": doc.id,
            "topic": data["topic"],
            "description": data["description"],
            "roadmap": data["roadmap"],
            "summary": data.get("summary", ""),
            "summary_audio_path": data.get("summary_audio_path"),
            "created_at": data["created_at"]
        }
    
    return None

# Welcome Session Database Functions
def save_welcome_session(guest_id, session_name, chat_history, collected_info, current_step):
    """Save welcome session to database"""
    if not db:
        print("[FIRESTORE] Database not configured, skipping save")
        return
    
    try:
        doc_ref = db.collection("welcome_sessions").document(guest_id)
        doc_ref.set({
            "guest_id": guest_id,
            "session_name": session_name,
            "chat_history": chat_history,
            "collected_info": collected_info,
            "current_step": current_step,
            "updated_at": datetime.now()
        }, merge=True)
        print(f"[FIRESTORE] Welcome session saved for guest: {guest_id}")
    except Exception as e:
        print(f"[FIRESTORE] Failed to save welcome session: {e}")

def get_welcome_session_from_db(guest_id):
    """Get welcome session from database"""
    if not db:
        return None
    
    try:
        doc_ref = db.collection("welcome_sessions").document(guest_id)
        doc = doc_ref.get()
        
        if doc.exists:
            return doc.to_dict()
        return None
    except Exception as e:
        print(f"[FIRESTORE] Failed to get welcome session: {e}")
        return None