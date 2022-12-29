import random
from typing import List, Optional

from velvet_dawn import errors


""" Tile textures data

Tiles must have a color but also a possible assignable overlay image.
A tile may be defined with a list of colors/images but only one will
be chosen when the tile is created.
"""


AVAILABLE_KEYS = {"color", "image", "notes"}


class TileTextures:
    def __init__(self):
        self.colors: List[str] = []
        self.images: List[str] = []

    def choose_color(self) -> Optional[str]:
        """ Choose the tile color

        Returns:
            The chosen color
        """
        return random.choice(self.colors)

    def choose_image(self) -> Optional[str]:
        """ Choose the image

        Returns:
            The chosen image
        """
        if not self.images:
            return None

        choice = random.choice(self.images)
        if choice == "null":
            return None

        return choice

    @staticmethod
    def load(tile_id: str, data: dict):
        """ Parse the data for load the colors and textures """
        textures = TileTextures()

        background_colors = data.get("color", "#0099ff")
        if isinstance(background_colors, str): textures.colors = [background_colors]
        elif isinstance(background_colors, list): textures.colors = background_colors
        elif isinstance(background_colors, dict):
            for key in background_colors:
                textures.colors += [key] * background_colors[key]
        else:
            raise errors.ValidationError(f"{tile_id} has invalid background textures.")

        background_textures = data.get("image")
        if isinstance(background_textures, str): textures.images = [background_textures]
        elif isinstance(background_textures, list): textures.images = background_textures
        elif isinstance(background_textures, dict):
            for key in background_textures:
                textures.images += [key] * background_textures[key]
        elif background_textures is None: pass
        else:
            raise errors.ValidationError(f"{tile_id} has invalid background textures.")

        # Check for random other keys
        for key in data:
            if key not in AVAILABLE_KEYS:
                raise errors.ValidationError(f"{tile_id} textures unknown key: '{key}'")

        return textures
