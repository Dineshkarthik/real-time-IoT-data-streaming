import json
import socket
from datetime import datetime

from kafka import KafkaProducer


UDP_IP = ""
UDP_PORT = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
kafka_producer = KafkaProducer(
    bootstrap_servers=["kafka:9092"],
    value_serializer=lambda x: json.dumps(x).encode("ascii"),
)

while True:
    data, addr = sock.recvfrom(1024)
    row = data.decode("utf-8").split(",")
    print(row)
    payload = {
        "timestamp": datetime.now().isoformat(),
        "sender": addr[0],
        "data": {
            "_id": row[0].replace(".", ""),
            "accelerometer": (float(row[2]), float(row[3]), float(row[4])),
        },
    }
    if len(row) > 5:
        payload["data"]["gyroscope"] = (
            float(row[6]),
            float(row[7]),
            float(row[8]),
        )

    if len(row) > 9:
        payload["data"]["magnetic_field"] = (
            float(row[10]),
            float(row[11]),
            float(row[12]),
        )
    kafka_producer.send("my-topic", payload)
