import os
import tempfile
from groq import Groq
from pydub import AudioSegment

# Initialize Groq Client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def transcribe_audio(file_path: str) -> str:
    """
    Sends audio file to Groq API for transcription using whisper-large-v3.
    """
    try:
        with open(file_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(os.path.basename(file_path), file.read()),
                model="whisper-large-v3",
                response_format="json",
                # language="en",  <-- Removed to allow auto-detection for Yoruba, Igbo, Hausa
                temperature=0.0
            )
        return transcription.text
    except Exception as e:
        print(f"Groq Transcription Error: {e}")
        return "Oga, I no hear you clear. Type am abeg."

def process_audio(file_path: str) -> str:
    """
    Converts audio file to WAV (if needed) and transcribes using Groq.
    """
    wav_path = None
    try:
        # Check if conversion is needed (Groq supports many formats, but let's encourage WAV/MP3)
        filename, ext = os.path.splitext(file_path)
        
        # If it's already a compatible format, pass directly? 
        # Groq supports ogg, but users might send voice notes in .oga or .ogg (opus).
        # To be safe, let's keep the conversion to wav.
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as wav_file:
            wav_path = wav_file.name
            
        audio = AudioSegment.from_file(file_path)
        audio.export(wav_path, format="wav")
        
        # Transcribe
        text = transcribe_audio(wav_path)
        return text.strip()
        
    except Exception as e:
        print(f"Error processing audio: {e}")
        return "Oga, I no hear you clear. Type am abeg."
        
    finally:
        # Cleanup temp wav file
        if wav_path and os.path.exists(wav_path):
            os.remove(wav_path)
        # We don't delete the original file_path here as it might be managed by the caller

