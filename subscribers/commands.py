import json
from loguru import logger


class CommandsSubscriber:
    def __init__(self, settings, client):
        self.settings = settings
        self.client = client
        self.commands = {}
        self.topic = f"gnosis/{self.settings['workspace_id']}/devices/{self.settings['device_id']}/commands"

    async def handle(self, message):
        command = json.loads(message)
        logger.info("Received command: {}", message)