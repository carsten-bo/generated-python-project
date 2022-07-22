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
