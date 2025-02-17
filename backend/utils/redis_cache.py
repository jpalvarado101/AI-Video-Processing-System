# backend/utils/redis_cache.py
import redis
import json

try:
    r = redis.Redis(host='localhost', port=6379, db=0)
    # Test connection with a simple ping
    r.ping()
except Exception as e:
    print("Redis not available, skipping caching:", e)
    r = None

def cache_result(video_filename, scene):
    """
    Cache the best scene result using the video filename as the key.
    If Redis is not available, this function does nothing.
    """
    if r is None:
        return  # Skip caching if Redis is not set up
    data = {"scene": scene}
    r.set(video_filename, json.dumps(data))
