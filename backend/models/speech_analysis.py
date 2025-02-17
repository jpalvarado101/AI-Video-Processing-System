# backend/models/speech_analysis.py
import subprocess
import os
import whisper
from transformers import pipeline

# Load Whisper model (using the open-source version)
whisper_model = whisper.load_model("base")  # adjust model size as needed

# Load a sentiment analysis pipeline from Hugging Face
sentiment_pipeline = pipeline("sentiment-analysis")

def analyze_audio(video_path):
    """
    Extracts audio from video, transcribes it, and analyzes sentiment.
    Returns a transcript and a list of sentiment results.
    """
    # Define audio path (assumes video is .mp4; adjust if needed)
    base, _ = os.path.splitext(video_path)
    audio_path = base + ".wav"
    
    # Extract audio using FFmpeg (ensure ffmpeg is installed)
    subprocess.call(["ffmpeg", "-y", "-i", video_path, audio_path])
    
    # Transcribe audio with Whisper
    result = whisper_model.transcribe(audio_path)
    transcript = result["text"]
    
    # Run sentiment analysis on the transcript
    sentiments = sentiment_pipeline(transcript)
    
    # Optionally remove temporary audio file
    # os.remove(audio_path)
    
    return transcript, sentiments
