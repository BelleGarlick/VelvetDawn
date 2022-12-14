import json
import dataclasses
from typing import List

from pathlib import Path


@dataclasses.dataclass
class Config:

    port: int = 1651
    password: str = 'bananana'
    datapacks: List[str] = None
    turn_time: int = 120

    @staticmethod
    def load():
        config = Config()

        config_path = Path(__file__).parent.parent / "velvet-dawn.config.json"
        with open(config_path) as file:
            data = json.load(file)

            for key in data:
                setattr(config, key, data[key])

        return config
