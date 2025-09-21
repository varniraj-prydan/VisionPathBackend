import os
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv()

# Print to verify env vars are loaded
print(f"Project ID: {os.getenv('GOOGLE_CLOUD_PROJECT')}")
print(f"Credentials: {os.getenv('GOOGLE_APPLICATION_CREDENTIALS')}")

from services.speech_service import transcribe_audio
from services.gemini_service import generate_roadmap
from services.tts_service import generate_audio
from services.firestore_service import save_roadmap, get_lesson

def test_tts():
    """Test Text-to-Speech"""
    print("Testing TTS...")
    try:
        audio_path = generate_audio("Hello, This is vision path ,Tell me Your goal you want to learn,In how many days,Description and what you wanted to be")
        print(f"✓ TTS working - Audio saved to: {audio_path}")
        return True
    except Exception as e:
        print(f"✗ TTS failed: {e}")
        return False

def test_gemini():
    """Test Gemini roadmap generation"""
    print("Testing Gemini...")
    try:
        roadmap = generate_roadmap("Python", "Learn Python basics")
        print(f"✓ Gemini working - Generated roadmap with {len(roadmap.get('days', []))} days")
        print(f"Roadmap: {roadmap}")
        return True, roadmap
    except Exception as e:
        print(f"✗ Gemini failed: {e}")
        return False, None

def test_firestore(roadmap):
    """Test Firestore save/get"""
    print("Testing Firestore...")
    try:
        roadmap_id = save_roadmap("Python", "Test description", roadmap)
        print(f"✓ Firestore save working - ID: {roadmap_id}")
        
        lesson = get_lesson(roadmap_id, 1)
        print(f"✓ Firestore get working - Retrieved lesson")
        return True
    except Exception as e:
        print(f"✗ Firestore failed: {e}")
        return False

def test_speech_with_sample():
    """Test Speech-to-Text with sample audio"""
    print("Testing Speech-to-Text...")
    print("Note: Need actual audio file to test. Create a test.wav file or skip this test.")
    
    audio_file = "audio/lesson_353.wav"
    if os.path.exists(audio_file):
        try:
            with open(audio_file, "rb") as f:
                audio_bytes = f.read()
            transcript = transcribe_audio(audio_bytes)
            print(f"✓ Speech-to-Text working - Transcript: {transcript}")
            return True
        except Exception as e:
            print(f"✗ Speech-to-Text failed: {e}")
            return False
    else:
        print(f"⚠ Speech-to-Text test skipped - {audio_file} not found")
        return True

if __name__ == "__main__":
    print("=== Testing All Services ===\n")
    
    # Test TTS
    # tts_ok = test_tts()
    # print()
    
    # Test Gemini
    gemini_ok, roadmap = test_gemini()
    print()
    
    # # Test Firestore
    # firestore_ok = test_firestore(roadmap) if roadmap else False
    # print()
    
    # # Test Speech
    # speech_ok = test_speech_with_sample()
    # print()
    
    print("=== Results ===")
    print(f"TTS: {'✓' if tts_ok else '✗'}")
    # print(f"Gemini: {'✓' if gemini_ok else '✗'}")
    # print(f"Firestore: {'✓' if firestore_ok else '✗'}")
    # print(f"Speech: {'✓' if speech_ok else '✗'}")
    
    if all([tts_ok]):
        print("\n🎉 All services working!")
    else:
        print("\n⚠ Some services need attention")