from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from services.speech_service import transcribe_audio
from services.gemini_service import generate_roadmap
from services.tts_service import generate_audio
from services.firestore_service import save_roadmap, get_lesson, get_all_roadmaps, get_single_roadmap
from services.session_service import create_session, add_audio_to_session, cleanup_session
from services.welcome_service import create_welcome_session, process_welcome_input, generate_roadmap_from_session

load_dotenv()

# Debug environment variables
print(f"[ENV] GOOGLE_APPLICATION_CREDENTIALS: {os.getenv('GOOGLE_APPLICATION_CREDENTIALS')}")
print(f"[ENV] GOOGLE_CLOUD_PROJECT: {os.getenv('GOOGLE_CLOUD_PROJECT')}")

app = FastAPI(title="Voice Learning Tutor API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RoadmapRequest(BaseModel):
    prompt:str

class TTSRequest(BaseModel):
    text: str
    session_id: str = None

class SessionRequest(BaseModel):
    session_id: str

class WelcomeRequest(BaseModel):
    guest_id: str
    user_input: str

class RoadmapGenerationRequest(BaseModel):
    learning_summary: str

@app.post("/capture")
async def capture_audio(audio: UploadFile = File(...)):
    try:
        print(f"[CAPTURE] Received file: {audio.filename}")
        print(f"[CAPTURE] Content type: {audio.content_type}")
        print(f"[CAPTURE] File size: {audio.size} bytes")
        
        audio_bytes = await audio.read()
        print(f"[CAPTURE] Read {len(audio_bytes)} bytes from file")
        
        transcript = transcribe_audio(audio_bytes)
        print(f"[CAPTURE] Transcript result: {transcript}")
        
        return {"transcript": transcript}
    except Exception as e:
        print(f"[CAPTURE] Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

class RoadmapRequest(BaseModel):
    prompt: str
    session_id: str = None

@app.post("/create-roadmap")
async def create_roadmap(request: RoadmapRequest):
    try:
        roadmap_json = generate_roadmap(request.prompt)
        day1_lesson = roadmap_json["days"][0]["lesson"]
        audio_path = generate_audio(day1_lesson)
        
        summary = roadmap_json.get("summary", "")
        summary_audio_path = generate_audio(summary) if summary else None
        
        # Add audio files to session for cleanup
        if request.session_id:
            add_audio_to_session(request.session_id, audio_path)
            if summary_audio_path:
                add_audio_to_session(request.session_id, summary_audio_path)
        
        roadmap_id = save_roadmap(roadmap_json["topic"], request.prompt, roadmap_json, summary, summary_audio_path)
        
        return {
            "roadmap_id": roadmap_id,
            "roadmap": roadmap_json,
            "day1_audio_url": f"/audio/{os.path.basename(audio_path)}",
            "summary_audio_url": f"/audio/{os.path.basename(summary_audio_path)}" if summary_audio_path else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get-lesson/{roadmap_id}/{day}")
async def get_lesson_endpoint(roadmap_id: str, day: int):
    try:
        lesson = get_lesson(roadmap_id, day)
        return lesson
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/create-session")
async def create_audio_session():
    try:
        session_id = create_session()
        return {"session_id": session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/text-to-speech")
async def text_to_speech(request: TTSRequest):
    try:
        audio_path = generate_audio(request.text)
        if request.session_id:
            add_audio_to_session(request.session_id, audio_path)
        return {"audio_url": f"/audio/{os.path.basename(audio_path)}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/cleanup-session")
async def cleanup_audio_session(request: SessionRequest):
    try:
        success = cleanup_session(request.session_id)
        return {"success": success, "message": "Session cleaned up" if success else "Session not found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/roadmaps")
async def get_roadmaps():
    try:
        roadmaps = get_all_roadmaps()
        return {"roadmaps": roadmaps}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/roadmap/{roadmap_id}")
async def get_roadmap(roadmap_id: str):
    try:
        roadmap = get_single_roadmap(roadmap_id)
        if roadmap:
            return roadmap
        raise HTTPException(status_code=404, detail="Roadmap not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/roadmap-summary-audio/{roadmap_id}")
async def get_roadmap_summary_audio(roadmap_id: str):
    try:
        roadmap = get_single_roadmap(roadmap_id)
        if roadmap and roadmap.get("summary_audio_path"):
            audio_path = roadmap["summary_audio_path"]
            if os.path.exists(audio_path):
                return FileResponse(audio_path, media_type="audio/wav")
        raise HTTPException(status_code=404, detail="Summary audio not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/welcome/start")
async def start_welcome_session():
    try:
        guest_id, welcome_message, audio_url = create_welcome_session()
        return {
            "guest_id": guest_id,
            "message": welcome_message,
            "audio_url": audio_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/welcome/chat")
async def welcome_chat(request: WelcomeRequest):
    try:
        result = process_welcome_input(request.guest_id, request.user_input)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/welcome/generate-roadmap")
async def generate_welcome_roadmap(request: RoadmapGenerationRequest):
    try:
        # Generate roadmap directly from learning summary
        roadmap_json = generate_roadmap(request.learning_summary)
        day1_lesson = roadmap_json["days"][0]["lesson"]
        audio_path = generate_audio(day1_lesson)
        
        summary = roadmap_json.get("summary", "")
        summary_audio_path = generate_audio(summary) if summary else None
        
        roadmap_id = save_roadmap(roadmap_json["topic"], request.learning_summary, roadmap_json, summary, summary_audio_path)
        
        return {
            "roadmap_id": roadmap_id,
            "roadmap": roadmap_json,
            "day1_audio_url": f"/audio/{os.path.basename(audio_path)}",
            "summary_audio_url": f"/audio/{os.path.basename(summary_audio_path)}" if summary_audio_path else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    audio_path = f"audio/{filename}"
    if os.path.exists(audio_path):
        return FileResponse(audio_path, media_type="audio/wav")
    raise HTTPException(status_code=404, detail="Audio file not found")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)