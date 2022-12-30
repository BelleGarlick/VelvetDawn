from typing import Dict

from velvet_dawn.models.datapacks.custom_attributes import CustomAttributes
from velvet_dawn.models.datapacks.taggable import Taggable
from velvet_dawn.models.datapacks.tiles.tile_movement import TileMovement
from velvet_dawn.models.datapacks.tiles.tile_textures import TileTextures


# TODO Test tile, entity and resource loading


class Tile(Taggable):
    def __init__(self, id: str, name: str):
        super().__init__()

        self.id: str = id
        self.name: str = name
        self.neighbours: Dict[str, int] = {}
        self.textures = TileTextures()
        self.movement: TileMovement = TileMovement()

        self.attributes = CustomAttributes()

    def json(self):
        # Textures not returned, since they're returned in the entity instance,
        # so not needed here
        return {
            "id": self.id,
            "name": self.name,
            "attributes": self.attributes.json(),
            "movement": self.movement.json()
        }

    @staticmethod
    def load(tile_id: str, data: dict):
        tile = Tile(
            id=tile_id,
            name=data['name']
        )

        tile.traversable = data.get("traversable", True)
        tile.neighbours = data['neighbours']
        tile.attributes = CustomAttributes.load(tile_id, data.get('attributes', []))
        tile.textures = TileTextures.load(tile_id, data.get('textures', {}))
        tile.movement = TileMovement.load(tile_id, data.get("movement", {}))

        tile._load_tags(data)

        return tile
