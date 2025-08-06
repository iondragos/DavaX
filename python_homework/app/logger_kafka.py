import os
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP", "localhost:9092"),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_log(payload: dict):
    try:
        producer.send("math-requests", payload)
        producer.flush()
        print("Kafka log sent:", payload)
    except Exception as e:
        print("Kafka send error:", str(e))