# backend/utils/video_processing.py
import cv2

def detect_scenes(video_path, threshold=30.0):
    """
    Detect scene changes by computing frame differences.
    Returns a list of (start_time, end_time) tuples in seconds.
    """
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    scenes = []
    ret, prev_frame = cap.read()
    if not ret:
        cap.release()
        return scenes

    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    scene_start = 0
    current_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            # End of video: add final scene
            scenes.append((scene_start, current_time))
            break
        current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(prev_gray, gray)
        non_zero_count = cv2.countNonZero(diff)
        # If a significant difference is detected, mark a scene change
        if non_zero_count > threshold * diff.size / 100:
            scenes.append((scene_start, current_time))
            scene_start = current_time
        prev_gray = gray

    cap.release()
    return scenes
