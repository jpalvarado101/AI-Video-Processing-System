import torch
import whisper
import clip
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"

def load_clip_model():
    model, preprocess = clip.load("ViT-B/32", device=device)
    return model, preprocess

def transcribe_audio(video_path):
    model = whisper.load_model("base", device=device)
    
    audio_path = video_path.replace(".mp4", ".wav")
    ffmpeg.input(video_path).output(audio_path, format='wav').run()
    
    result = model.transcribe(audio_path)
    return result["text"]
