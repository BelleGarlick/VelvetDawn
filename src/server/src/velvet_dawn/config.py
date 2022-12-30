import json
import dataclasses
from typing import List

from pathlib import Path


@dataclasses.dataclass
class SpawningConfig:
    width_multiplier = 2
    width_addition = 2
    neighbours_multiplier = 2

    def set_spawning(self, width_multiplier, width_addition, neighbours_multiplier):
        self.width_multiplier = width_multiplier
        self.width_addition = width_addition
        self.neighbours_multiplier = neighbours_multiplier
        return self


class Config:

    def __init__(self):
        self.seed = None

        self.port: int = 1651
        self.datapacks: List[str] = []

        self.turn_time: int = 300
        self.setup_time: int = 300

        self.map_width = 31
        self.map_height = 19

        self.spawning: SpawningConfig = SpawningConfig()

    @staticmethod
    def load():
        config = Config()
        config.spawning = SpawningConfig()

        config_path = Path(__file__).parent.parent.parent.parent.parent / "velvet-dawn.config.json"
        with open(config_path) as file:
            data = json.load(file)

            for key in data:
                setattr(config, key, data[key])

            map_data = data.get("map", {})
            config.map_width = map_data.get("width", config.map_width)
            config.map_height = map_data.get("height", config.map_height)

        return config

    def set_map_size(self, map_width, map_height):
        self.map_width = map_width
        self.map_height = map_height
        return self
