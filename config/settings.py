import json
import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = Path(__file__).resolve().parent

def _env_bool(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "yes", "on")

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
        "ssl_use": _env_bool("SSL_USE"),
        "iot_base_url": os.getenv("IOT_BASE_URL"),
        "device_id": device.get("device_id"),
        "workspace_id": device.get("workspace_id"),
        "name": device.get("name"),
        "beacond_url": os.getenv("BEACOND_URL"),
    }