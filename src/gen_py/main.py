import json
import time

buffer = []


def receive_message(msg: str):
    try:
        if len(msg) > 4096:
            return
        data = json.loads(msg)
        for pkg in data:
            process_package(pkg)
    except ValueError:
        pass


def process_package(pkg: dict):
    verify_package(pkg)
    buffer.append(pkg)
    if len(buffer) >= 10:
        flush_buffer()


def verify_package(pkg: dict):
    if 'temperature' not in pkg:
        raise ValueError()
    if not (-30 < pkg['temperature'] < 150):
        raise ValueError()
    if 'timestamp' not in pkg:
        raise ValueError()
    if not pkg['timestamp'] < time.time():
        raise ValueError()


def flush_buffer():
    for b in buffer:
        print(b)
    buffer.clear()


if __name__ == '__main__':
    receive_message("""[
        {
            "timestamp": 1635875212060,
            "payload": {
                "temperature": 3.986548233191974, 
                "sensorId": "Sensor-74ed4a6d-5957-4a2d-b02f-9122fd66c92a"
            }
        },
        {
            "timestamp": 1635875212024,
            "payload": {
                "temperature": -0.17564610049023222, 
                "sensorId": "Sensor-45af12c9-2abe-472d-9ca3-9ea215fc9d10"
            }
        },
    ]
    """)