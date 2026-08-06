import asyncio

import aiomqtt
from loguru import logger


class MQTTClient:
    def __init__(self, settings):
        self.mqtt_host = settings["mqtt_host"]
        self.mqtt_port = settings["mqtt_port"]
        self.mqtt_username = settings["mqtt_username"]
        self.mqtt_password = settings["mqtt_password"]
        self.device_id = settings["device_id"]
        self.workspace_id = settings["workspace_id"]
        self.client = None

    async def publish(self, topic, payload):
        logger.debug("Publishing to {}: {}", topic, payload)
        await self.client.publish(topic, payload)

    async def run(self, publishers):
        while True:
            try:
                logger.info(
                    "Connecting to MQTT broker {}:{}",
                    self.mqtt_host,
                    self.mqtt_port,
                )
                async with aiomqtt.Client(
                        self.mqtt_host,
                        self.mqtt_port,
                        username=self.mqtt_username,
                        password=self.mqtt_password,
                    ) as client:

                    self.client = client
                    logger.info("Connected to MQTT broker")

                    await asyncio.gather(
                        *(publisher.run() for publisher in publishers)
                    )
            except aiomqtt.MqttError as e:
                logger.warning("MQTT error, reconnecting in 3s: {}", e)
                await asyncio.sleep(3)
            except Exception as e:
                logger.exception("Unexpected MQTT client error, retrying in 3s: {}", e)
                await asyncio.sleep(3)
