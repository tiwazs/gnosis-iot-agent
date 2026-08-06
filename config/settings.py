import json
import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = Path(__file__).resolve().parent

def load_settings():
    load_dotenv(ROOT / ".env")
    
    device = {}
    device_path = CONFIG_DIR / "config.json"
    if device_path.exists():
        device = json.loads(device_path.read_text())
    return {
        "mqtt_host": os.getenv("MQTT_HOST", "localhost"),
        "mqtt_port": int(os.getenv("MQTT_PORT", "1883")),
        "mqtt_username": os.getenv("MQTT_USERNAME"),
        "mqtt_password": os.getenv("MQTT_PASSWORD"),
        "iot_base_url": os.getenv("IOT_BASE_URL"),
        "device_id": device.get("device_id"),
        "workspace_id": device.get("workspace_id"),
        "name": device.get("name")
    }