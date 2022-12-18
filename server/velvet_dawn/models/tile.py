import dataclasses
import json
from pathlib import Path
from typing import Dict


@dataclasses.dataclass
class Tile:

    id: str
    texture: str
    name: str
    traversable: bool = True
    neighbours: Dict[str, int] = None

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "texture": self.texture
        }

    @staticmethod
    def load(file_path):
        file_path = Path(file_path)
        with open(file_path) as file:
            data = json.load(file)

            tile = Tile(
                id=f"{file_path.parent.parent.stem}:{file_path.stem}",
                name=data['name'],
                texture=data['texture']
            )

            tile.traversable = data.get("traversalbe", True)
            tile.neighbours = data['neighbours']

            return tile
