# backend/models/clip_model.py
import torch
import clip
from PIL import Image
import cv2

# Load CLIP model and preprocessing (using the open-source version)
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def get_scene_image(video_path, scene):
    """
    Extract a frame (as PIL Image) from the video at the midpoint of the scene.
    'scene' is a tuple (start_time, end_time) in seconds.
    """
    start, end = scene
    mid = int((start + end) / 2 * 1000)  # convert seconds to milliseconds
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_MSEC, mid)
    ret, frame = cap.read()
    cap.release()
    if ret:
        # Convert BGR (OpenCV) to RGB (PIL)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return Image.fromarray(frame_rgb)
    return None

def score_scene(image, text_prompt="exciting moment"):
    """
    Use CLIP to score the image against a text prompt.
    """
    image_input = preprocess(image).unsqueeze(0).to(device)
    text_input = clip.tokenize([text_prompt]).to(device)

    with torch.no_grad():
        image_features = model.encode_image(image_input)
        text_features = model.encode_text(text_input)
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        similarity = (image_features @ text_features.T).item()
    return similarity

def get_best_scene(video_path, scenes):
    """
    Iterate over detected scenes, score each using CLIP, and return the scene tuple
    with the highest score.
    """
    best_score = -1
    best_scene = None
    for scene in scenes:
        image = get_scene_image(video_path, scene)
        if image is not None:
            score = score_scene(image)
            if score > best_score:
                best_score = score
                best_scene = scene
    return best_scene
