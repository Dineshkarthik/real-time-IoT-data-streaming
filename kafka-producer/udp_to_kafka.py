import json
import socket
import time
from datetime import datetime

from kafka import KafkaProducer


UDP_IP: str = ""
UDP_PORT: int = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# wait 15 secs for the kafka broker to be up & running
time.sleep(15)

kafka_producer = KafkaProducer(
    bootstrap_servers=["kafka:9092"],
    value_serializer=lambda x: json.dumps(x).encode("ascii"),
)

sensor_map: dict = {
    1: "gps_position",
    3: "accelerometer",
    4: "gyroscope",
    5: "magnetic_field",
    81: "orientation",
    82: "linear_acceleration",
    83: "gravity",
    84: "rotation_vector",
    85: "pressure",
    86: "battery_temperature",
}


def get_payload(row: list) -> dict:
    row: list = list(map(float, row))
    dict_: dict = {}
    for key in sensor_map:
        if key in row:
            _index: int = row.index(key)
            if key not in (85, 86):
                dict_[sensor_map[key]] = row[_index + 1 : _index + 4]
            else:
                dict_[sensor_map[key]] = row[_index + 1 : _index + 2][0]
    return dict_


while True:
    data, addr = sock.recvfrom(1024)
    row: list = data.decode("utf-8").split(",")
    payload: dict = get_payload(row)
    payload["@timestamp"] = datetime.now().isoformat()
    payload["sender"] = addr[0]
    payload["event_id"] = row[0].replace(".", "")
    kafka_producer.send("smartphone-sensor", payload)
