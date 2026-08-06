import asyncio
from loguru import logger

from config.logging_setup import setup_logging
from config.settings import load_settings
from mqtt.client import MQTTClient
from publishers.coordinates import CoordinatesPublisher


async def main():
    setup_logging()
    logger.info("Starting Gnosis IoT agent")

    settings = load_settings()
    if not settings.get("mqtt_host") or not settings.get("mqtt_port") or not settings.get("mqtt_username") or not settings.get("mqtt_password"):
        logger.error("MQTT credentials are not set")
        return
    if not settings.get("device_id") or not settings.get("workspace_id"):
        logger.error("Not registered. Run register first.")
        return

    logger.info(
        "Device ready device_id={} workspace_id={} name={}",
        settings["device_id"],
        settings["workspace_id"],
        settings.get("name"),
    )

    mqtt = MQTTClient(settings)
    coordinates_publisher = CoordinatesPublisher(settings, mqtt)

    logger.info("Launching publishers")
    await mqtt.run([coordinates_publisher])


if __name__ == "__main__":
    asyncio.run(main())
