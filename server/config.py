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


@dataclasses.dataclass
class Config:

    port: int = 1651
    password: str = 'bananana'
    datapacks: List[str] = None
    turn_time: int = 120

    map_width = 50
    map_height = 40

    spawning: SpawningConfig = SpawningConfig()

    @staticmethod
    def load():
        config = Config()
        config.spawning = SpawningConfig()

        config_path = Path(__file__).parent.parent / "velvet-dawn.config.json"
        with open(config_path) as file:
            data = json.load(file)

            for key in data:
                setattr(config, key, data[key])

        return config

    def set_map_size(self, map_width, map_height):
        self.map_width = map_width
        self.map_height = map_height
        return self
