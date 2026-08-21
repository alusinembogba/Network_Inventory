import json
from datetime import datetime

def load_health_history():
    try:
        with open("health_history.json", "r") as file:
            return json.load(file)

    except FileNotFoundError:
        return []

def record_health_check(devices):

    history = load_health_history()

    timestamp = datetime.now().strftime("%d %B %Y %H:%M:%S")

    for device in devices:

        record = {
            "timestamp": timestamp,
            "hostname": device["hostname"],
            "ip": device["ip"],
            "status": device["status"],
            "response_time": device["response_time"]
        }

        history.append(record)

    with open("health_history.json", "w") as file:
        json.dump(history, file, indent=4)

    print("Health check history saved.")
    
