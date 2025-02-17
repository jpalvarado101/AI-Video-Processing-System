# backend/app.py
import os
import shutil
from fastapi import FastAPI, File, UploadFile
import uvicorn

# Import our AI modules and utilities
from models import clip_model, speech_analysis, summarization
from utils import video_processing, kafka_producer, redis_cache

app = FastAPI()

@app.post("/process_video")
async def process_video(file: UploadFile = File(...)):
    # Save uploaded video locally
    os.makedirs("temp", exist_ok=True)
    video_path = os.path.join("temp", file.filename)
    with open(video_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # 1. Detect scene segments
    scenes = video_processing.detect_scenes(video_path)

    # 2. Extract audio, transcribe, and run sentiment analysis
    transcript, sentiments = speech_analysis.analyze_audio(video_path)

    # 3. Summarize transcript using a free summarization model (T5-small)
    caption = summarization.summarize_text(transcript)

    # 4. Use CLIP to score each scene and pick the best (most “exciting”) scene
    best_scene = clip_model.get_best_scene(video_path, scenes)

    # 5. For demonstration: send an event via Kafka and cache the result in Redis
    kafka_producer.send_video_processing_event(file.filename, best_scene)
    redis_cache.cache_result(file.filename, best_scene)

    # Return results (in a real app you might return the processed clip URL, etc.)
    return {"caption": caption, "best_scene": best_scene, "sentiments": sentiments}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
