from google.cloud import speech
from .auth_service import get_credentials

def transcribe_audio(audio_bytes):
    credentials = get_credentials()
    client = speech.SpeechClient(credentials=credentials) if credentials else speech.SpeechClient()
    
    print(f"[SPEECH] Processing {len(audio_bytes)} bytes")
    
    audio = speech.RecognitionAudio(content=audio_bytes)
    
    # Try multiple configurations for WebM
    configs = [
        # WebM Opus configuration
        speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
            sample_rate_hertz=48000,
            language_code="en-US",
            enable_automatic_punctuation=True,
        ),
        # Alternative WebM configuration
        speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
            sample_rate_hertz=16000,
            language_code="en-US",
            enable_automatic_punctuation=True,
        ),
        # Auto-detect encoding
        speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
            language_code="en-US",
            enable_automatic_punctuation=True,
        )
    ]
    
    for i, config in enumerate(configs):
        try:
            print(f"[SPEECH] Trying config {i+1}: {config.encoding.name}, sample_rate: {getattr(config, 'sample_rate_hertz', 'auto')}")
            response = client.recognize(config=config, audio=audio)
            
            print(f"[SPEECH] Response received: {len(response.results)} results")
            
            if response.results:
                transcript = response.results[0].alternatives[0].transcript
                confidence = response.results[0].alternatives[0].confidence
                print(f"[SPEECH] Success with config {i+1}: '{transcript}' (confidence: {confidence})")
                return transcript
            else:
                print(f"[SPEECH] Config {i+1}: No results")
                
        except Exception as e:
            print(f"[SPEECH] Config {i+1} failed: {str(e)}")
            continue
    
    print(f"[SPEECH] All configurations failed")
    return ""