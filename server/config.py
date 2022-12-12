import json
import dataclasses
from typing import List


@dataclasses.dataclass
class Config:

    port: int = 1651
    password: str = 'bananana'
    datapacks: List[str] = None
    turn_time: int = 120

    @staticmethod
    def load():
        config = Config()

        with open("../../velvet-dawn.config.json") as file:
            data = json.load(file)

            for key in data:
                setattr(config, key, data[key])

        return config
