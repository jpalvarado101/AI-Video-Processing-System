import cv2
import numpy as np
import torch
import torchvision.transforms as transforms
from models import load_clip_model, transcribe_audio
from PIL import Image
import ffmpeg

def extract_key_moments(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    prev_frame = None
    key_moments = []
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        if prev_frame is not None:
            diff = cv2.absdiff(gray, prev_frame)
            mean_diff = np.mean(diff)
            if mean_diff > 30:
                key_moments.append(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)
        
        prev_frame = gray
    
    cap.release()
    return key_moments

def generate_thumbnail(video_path):
    model, preprocess = load_clip_model()
    cap = cv2.VideoCapture(video_path)
    success, frame = cap.read()
    
    if success:
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        image = preprocess(image).unsqueeze(0).to("cuda")
        
        with torch.no_grad():
            features = model.encode_image(image)
        
        cap.release()
        return features.cpu().numpy().tolist()
    
    cap.release()
    return None

def process_video_file(video_path):
    key_moments = extract_key_moments(video_path)
    transcript = transcribe_audio(video_path)
    thumbnail = generate_thumbnail(video_path)
    
    return {"key_moments": key_moments, "transcript": transcript, "thumbnail": thumbnail}
