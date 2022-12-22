from typing import Dict

from velvet_dawn.models.datapacks.taggable import Taggable


class Tile(Taggable):
    def __init__(self, id: str, texture: str, name: str):
        super().__init__()

        self.id: str = id
        self.texture: str = texture
        self.name: str = name
        self.traversable: bool = True
        self.neighbours: Dict[str, int] = {}

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "texture": self.texture
        }

    @staticmethod
    def load(id: str, data: dict):
        tile = Tile(
            id=id,
            name=data['name'],
            texture=data['texture']
        )

        tile.traversable = data.get("traversable", True)
        tile.neighbours = data['neighbours']

        tile._load_tags(data)

        return tile
