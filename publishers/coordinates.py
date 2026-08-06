import json
import asyncio
from datetime import datetime

from loguru import logger


class CoordinatesPublisher:
    def __init__(self, settings, client):
        self.settings = settings
        self.client = client
        self.topic = f"gnosis/{self.settings['workspace_id']}/devices/{self.settings['device_id']}/coordinates"

    async def publish(self):
        coordinates = {
            "latitude": 0,
            "longitude": 0,
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
