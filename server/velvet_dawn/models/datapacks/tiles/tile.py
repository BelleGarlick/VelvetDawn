from typing import Dict
from velvet_dawn.models.datapacks.custom_attributes import CustomAttributes
from velvet_dawn.models.datapacks.taggable import Taggable
from velvet_dawn.models.datapacks.tiles.tile_textures import TileTextures


# TODO Test tile, entity and resource loading


class Tile(Taggable):
    def __init__(self, id: str, name: str):
        super().__init__()

        self.id: str = id
        self.name: str = name
        self.textures = TileTextures()
        self.traversable: bool = True
        self.neighbours: Dict[str, int] = {}

        self.attributes = CustomAttributes()

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "attributes": self.attributes.json()
        }

    @staticmethod
    def load(id: str, data: dict):
        tile = Tile(
            id=id,
            name=data['name']
        )

        tile.traversable = data.get("traversable", True)
        tile.neighbours = data['neighbours']
        tile.textures = TileTextures.load(id, data.get('textures', {}))
        tile.attributes.load(id, data.get('attributes', []))

        tile._load_tags(data)

        return tile
