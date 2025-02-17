from kafka import KafkaProducer
import json

try:
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
except Exception as e:
    print("Kafka not available, skipping Kafka producer setup:", e)
    producer = None

def send_video_processing_event(video_filename, scene):
    """
    Sends an event to the Kafka topic 'video_events' with video info.
    """
    if producer is None:
        return  # or log the event to a file or elsewhere

    event = {
        "video": video_filename,
        "scene": scene
    }
    producer.send("video_events", event)
    producer.flush()
