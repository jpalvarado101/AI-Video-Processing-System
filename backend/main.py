from fastapi import FastAPI, UploadFile, File
import torch
import whisper
import cv2
import numpy as np
import ffmpeg
import clip
from PIL import Image
import torch
import openai
import os
import tempfile
import redis
import psycopg2
from kafka import KafkaProducer
import json

# Initialize FastAPI app
app = FastAPI()

# Check if CUDA is available
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load OpenAI Whisper model for transcription
whisper_model = whisper.load_model("base").to(device)

# Load CLIP model for AI-based thumbnail selection
clip_model, preprocess = clip.load("ViT-B/32", device=device)

# Initialize Redis for caching
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# PostgreSQL database connection
conn = psycopg2.connect(
    dbname="video_db",
    user="postgres",
    password="password",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Function to extract key moments using OpenCV
def extract_key_moments(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    scene_changes = []
    prev_frame = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        if prev_frame is not None:
            diff = cv2.absdiff(gray, prev_frame)
            mean_diff = np.mean(diff)
            if mean_diff > 30:  # Threshold for scene change
                scene_changes.append(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)  # Convert to seconds
        
        prev_frame = gray
    
    cap.release()
    return scene_changes

# Function to transcribe audio
def transcribe_audio(video_path):
    audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    os.system(f"ffmpeg -i {video_path} -q:a 0 -map a {audio_file.name}")
    result = whisper_model.transcribe(audio_file.name)
    os.remove(audio_file.name)
    return result["text"]

# Function to select best thumbnail using CLIP
def select_best_thumbnail(video_path):
    cap = cv2.VideoCapture(video_path)
    best_score = -float("inf")
    best_frame = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert frame to PIL image
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        image_input = preprocess(image).unsqueeze(0).to(device)

        # CLIP scoring
        with torch.no_grad():
            text_features = clip_model.encode_text(clip.tokenize(["exciting moment"]).to(device))
            image_features = clip_model.encode_image(image_input)
            score = torch.cosine_similarity(text_features, image_features).item()
            
            if score > best_score:
                best_score = score
                best_frame = frame

    cap.release()

    # Save the best frame as a thumbnail
    thumbnail_path = "thumbnail.jpg"
    if best_frame is not None:
        cv2.imwrite(thumbnail_path, best_frame)
    return thumbnail_path

@app.post("/process_video/")
async def process_video(file: UploadFile = File(...)):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_file.write(await file.read())
    temp_file.close()
    
    video_path = temp_file.name
    key_moments = extract_key_moments(video_path)
    transcript = transcribe_audio(video_path)
    thumbnail_path = select_best_thumbnail(video_path)
    
    os.remove(video_path)
    
    redis_client.set(video_path, json.dumps({
        "key_moments": key_moments,
        "transcript": transcript,
        "thumbnail_path": thumbnail_path
    }), ex=3600)
    
    producer.send('video_processing', {"video_path": video_path, "key_moments": key_moments})
    
    cursor.execute("""
        INSERT INTO video_metadata (video_path, transcript, key_moments, thumbnail_path) VALUES (%s, %s, %s, %s)
    """, (video_path, transcript, json.dumps(key_moments), thumbnail_path))
    conn.commit()
    
    return {"key_moments": key_moments, "transcript": transcript, "thumbnail_path": thumbnail_path}
