import argparse
import os
import sys
import httpx
import json
DEFAULT_BASE_URL = os.getenv("IOT_BASE_URL", "http://localhost:3000")

def setup_device_config(device_id: str, workspace_id: str, name: str) -> None:
    config = {
        "device_id": device_id,
        "workspace_id": workspace_id,
        "name": name,
    }
    with open("config/config.json", "w") as f:
        json.dump(config, f)
    print("Device config file created")

def register(token: str, base_url: str) -> None:
    url = f"{base_url.rstrip('/')}/devices/register/{token}"
    with httpx.Client(timeout=10.0) as client:
        response = client.post(url)
    if response.is_success:
        device = response.json()
        
        setup_device_config(device.get('id'), device.get('workspace_id'), device.get('name'))

        print("Registered successfully")
        print(f"  device_id:    {device.get('id')}")
        print(f"  workspace_id: {device.get('workspace_id')}")
        print(f"  name:         {device.get('name')}")
        return True
    else:
        print("Failed to register device")
        return False

def main():
    parser = argparse.ArgumentParser(description="Register this device with Gnosis IoT")
    parser.add_argument("token", help="Registration code from the workspace (e.g. RPi-XXXX-XXXX)")
    parser.add_argument(
        "--url",
        default=DEFAULT_BASE_URL,
        help=f"IoT service base URL (default: {DEFAULT_BASE_URL})",
    )
    args = parser.parse_args()

    result = register(args.token, args.url)
    if result:
        sys.exit(0)
    else:
        sys.exit(1)
if __name__ == "__main__":
    main()