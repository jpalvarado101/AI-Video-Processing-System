import psycopg2
import redis
import json

# PostgreSQL Connection
conn = psycopg2.connect(
    dbname="video_db",
    user="postgres",
    password="password",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Redis Caching
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def save_video_metadata(video_path, result):
    cursor.execute("""
        INSERT INTO video_metadata (video_path, transcript, key_moments, thumbnail) VALUES (%s, %s, %s, %s)
    """, (video_path, result["transcript"], json.dumps(result["key_moments"]), json.dumps(result["thumbnail"])))
    conn.commit()
    redis_client.set(video_path, json.dumps(result), ex=3600)
