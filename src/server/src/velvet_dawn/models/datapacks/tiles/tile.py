from typing import Dict

import velvet_dawn
from velvet_dawn import errors
from velvet_dawn.models.datapacks.attributes import Attributes
from velvet_dawn.models.datapacks.tags import Tags
from .tile_textures import TileTextures

VALID_TILE_KEYS = [
    "id", "name", "abstract", "extends", "neighbours", "movement", "textures", "triggers", "tags", "notes"
]

VALID_MOVEMENT_KEYS = ["traversable", "weight", "notes"]


def _parse_movement(tile_id: str, attributes: Attributes, data: dict):
    """ Parse the tile movement data, see wiki for more information. """
    for key in data:
        if key not in VALID_MOVEMENT_KEYS:
            raise errors.ValidationError(f"Invalid movement key '{key}' on '{tile_id}'")

    # Extract
    traversable = data.get("traversable", True)
    weight = data.get("weight", 1)

    # Validate
    velvet_dawn.validations.is_number(weight, min=1, error_prefix=f"{tile_id} movement weight")
    velvet_dawn.validations.is_bool(traversable, error_prefix=f"{tile_id} movement transferability")

    # Set
    attributes.set("movement.traversable", value=traversable)
    attributes.set("movement.weight", value=weight)


class Tile:
    def __init__(self, id: str, name: str):
        from velvet_dawn.mechanics.triggers import Triggers

        super().__init__()

        self.id: str = id
        self.name: str = name
        self.neighbours: Dict[str, int] = {}
        self.textures = TileTextures()

        self.tags = Tags()
        self.attributes = Attributes()
        self.triggers = Triggers()

    def json(self):
        # Textures not returned, since they're returned in the entity instance,
        # so not needed here
        return {
            "id": self.id,
            "name": self.name,
            "attributes": self.attributes.json()
        }

    @staticmethod
    def load(tile_id: str, data: dict):
        for key in data:
            if key not in VALID_TILE_KEYS:
                raise errors.ValidationError(f"Invalid key '{key}' on entity '{tile_id}'")

        tile = Tile(
            id=tile_id,
            name=data['name']
        )

        tile.neighbours = data['neighbours']

        _parse_movement(tile_id, tile.attributes, data.get('movement', {}))
        tile.textures = TileTextures.load(tile_id, data.get('textures', {}))

        tile.attributes.load(tile_id, data.get('attributes', []))
        tile.triggers.load(tile_id, Tile, data.get("triggers", {}))

        tile.tags.load(tile_id, data.get('tags', []))

        return tile
