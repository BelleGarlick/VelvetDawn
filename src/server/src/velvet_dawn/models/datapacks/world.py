from velvet_dawn.logger import logger
from velvet_dawn.mechanics.triggers import Triggers


""" The global world definition, used for storing
trigger definitions performed on the WorldInstance
"""


class WorldDefinition:

    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(WorldDefinition, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.triggers = Triggers()

    def load(self, id: str, data: dict):
        """ Parse the world data for the given datapack """
        logger.info(f"Loading world triggers for: {id}")
        self.triggers.load(id, data.get("triggers", {}))
