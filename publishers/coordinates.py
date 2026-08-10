import json
import asyncio
from datetime import datetime

from loguru import logger

import subprocess
import requests


class CoordinatesPublisher:
    def __init__(self, settings, client):
        self.settings = settings
        self.client = client
        self.topic = f"gnosis/{self.settings['workspace_id']}/devices/{self.settings['device_id']}/coordinates"

    async def publish(self):
        coordinates = await self.get_coordinates()
        if coordinates:
            coordinates = {
                "latitude": coordinates["location"]["lat"],
                "longitude": coordinates["location"]["lng"],
                "altitude": 0,
                "speed": 0,
                "heading": 0,
                "timestamp": datetime.now().isoformat(),
            }
            
        await self.client.publish(self.topic, json.dumps(coordinates))
        logger.debug("Coordinates published to {}", self.topic)

    async def run(self):
        logger.info("Coordinates publisher started topic={}", self.topic)
        while True:
            try:
                await self.publish()
                await asyncio.sleep(5)
            except Exception as e:
                logger.exception("Error publishing coordinates: {}", e)
                await asyncio.sleep(3)

    async def wifi_scan(self):
        out = subprocess.check_output(
            ["nmcli", "-t", "-f", "BSSID,SIGNAL", "device", "wifi", "list"],
            text = True
        )

        scan = []

        for line in out.splitlines():
            if not line.strip():
                continue

            bssid, signal = line.rsplit(":", 1)
            bssid = bssid.replace("\\:", ":")
            scan.append({
                "macAddress": bssid,
                "signalStrength": int(signal) - 100,
            })

        return scan

    async def get_coordinates(self):
        scan = await self.wifi_scan()
        
        payload = {
            "wifiAccessPoints": scan,
            "fallbacks": {"ipf": True}
        }

        headers = {"User-Agent": "gnosis-iot-agent/1.0"}

        response = requests.post(
            self.settings["beacond_url"],
            json=payload,
            headers=headers,  # they ask you to set one
            timeout=10,
        )

        response = response.json()
        print(response)
        return response

    