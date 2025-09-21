from google.cloud import texttospeech
import os

def generate_audio(text):
    client = texttospeech.TextToSpeechClient()
    
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )
    
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    
    os.makedirs("audio", exist_ok=True)
    audio_path = f"audio/lesson_{hash(text) % 10000}.wav"
    
    with open(audio_path, "wb") as out:
        out.write(response.audio_content)
    
    return audio_path