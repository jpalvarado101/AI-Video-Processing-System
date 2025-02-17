from fastapi import FastAPI, UploadFile, File
import json
import os
import tempfile
import torch
from process_video import process_video_file
from database import save_video_metadata

app = FastAPI()

@app.post("/process_video/")
async def process_video_endpoint(file: UploadFile = File(...)):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_file.write(await file.read())
    temp_file.close()
    
    result = process_video_file(temp_file.name)
    
    save_video_metadata(temp_file.name, result)

    os.remove(temp_file.name)
    return result
