import argparse
import os
import sys
import httpx
import json
from loguru import logger


from config.logging_setup import setup_logging
from config.settings import load_settings

def setup_device_config(device_id: str, workspace_id: str, name: str) -> None:
    config = {
        "device_id": device_id,
        "workspace_id": workspace_id,
        "name": name,
    }
    with open("config/config.json", "w") as f:
        json.dump(config, f)
    logger.info("Device config written to config/config.json")


def register(token: str, base_url: str) -> None:

    if os.path.exists("config/config.json"):
        with open("config/config.json") as f:
            existing = json.load(f)
        if existing.get("device_id"):
            logger.error("Already registered: {}", existing["device_id"])
            sys.exit(1)

    url = f"{base_url.rstrip('/')}/devices/register/{token}"
    logger.info("Registering device at {}", url)
    with httpx.Client(timeout=10.0) as client:
        response = client.post(url)
    if response.is_success:
        device = response.json()

        setup_device_config(device.get('id'), device.get('workspace_id'), device.get('name'))

        logger.info(
            "Registered successfully device_id={} workspace_id={} name={}",
            device.get("id"),
            device.get("workspace_id"),
            device.get("name"),
        )
        return True
    else:
        logger.error(
            "Registration failed status={} body={}",
            response.status_code,
            response.text,
        )
        return False


def main():
    setup_logging()
    settings = load_settings()
    parser = argparse.ArgumentParser(description="Register this device with Gnosis IoT")
    parser.add_argument("token", help="Registration code from the workspace (e.g. RPi-XXXX-XXXX)")
    parser.add_argument(
        "--url",
        default=settings["iot_base_url"],
        help=f"IoT service base URL (default: {settings['iot_base_url']})",
    )
    args = parser.parse_args()

    result = register(args.token, args.url)
    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
