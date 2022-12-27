import random
from typing import Dict, List, Optional

from velvet_dawn import errors
from velvet_dawn.models.datapacks.taggable import Taggable


# TODO Test tile, entity and resource loading


class TileTextures:
    def __init__(self):
        self.color: List[str] = ["#0099ff"]
        self.background: List[str] = []

    def choose_color(self) -> Optional[str]:
        return random.choice(self.color)

    def choose_background(self) -> Optional[str]:
        if not self.background:
            return None

        choice = random.choice(self.background)
        if choice == "__empty__":
            return None

        return choice

    @staticmethod
    def load(tile_id: str, data: dict):
        textures = TileTextures()

        background_colors = data.get("color", "#0099ff")
        if isinstance(background_colors, str): textures.color = [background_colors]
        elif isinstance(background_colors, list): textures.color = background_colors
        elif isinstance(background_colors, dict):
            for key in background_colors:
                textures.color += [key] * background_colors[key]
        else:
            raise errors.ValidationError(f"{tile_id} has invalid background textures.")

        background_textures = data.get("background")
        if isinstance(background_textures, str): textures.background = [background_textures]
        elif isinstance(background_textures, list): textures.background = background_textures
        elif isinstance(background_textures, dict):
            for key in background_textures:
                textures.background += [key] * background_textures[key]
        elif background_textures is None: pass
        else:
            raise errors.ValidationError(f"{tile_id} has invalid background textures.")

        return textures


class Tile(Taggable):
    def __init__(self, id: str, name: str):
        super().__init__()

        self.id: str = id
        self.name: str = name
        self.textures = TileTextures()
        self.traversable: bool = True
        self.neighbours: Dict[str, int] = {}

    def json(self):
        return {
            "id": self.id,
            "name": self.name
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

        tile._load_tags(data)

        return tile
