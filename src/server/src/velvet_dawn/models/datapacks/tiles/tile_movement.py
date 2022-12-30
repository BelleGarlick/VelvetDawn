from velvet_dawn import errors


# TODO Test and document
# Test all permiatations and erronous keys


""" Tile Movement

Defines the movement data for a tile. 
For now the only attributes are weight and transferability,
which by default is 1. Higher penalties will take up higher
amounts of unit movement bandwidth 
"""


AVAILABLE_KEYS = {"weight", "traversable", "notes"}


class TileMovement:
    def __init__(self):
        self.weight: int = 1
        self.traversable = True

    def json(self):
        return {
            "weight": self.weight,
            "traversable": self.traversable
        }

    @staticmethod
    def load(tile_id: str, data: dict):
        """ Parse the movement data for a tile """
        movement = TileMovement()

        movement.weight = data.get("weight", 1)
        movement.traversable = data.get("traversable", True)

        if not isinstance(movement.weight, int):
            raise errors.ValidationError(f"{tile_id} movement weight must be a number.")
        if movement.weight < 1:
            raise errors.ValidationError(f"{tile_id} movement weight must be at least 1.")

        if not isinstance(movement.traversable, bool):
            raise errors.ValidationError(f"{tile_id} movement transferability must be either true or false.")

        # Check for random other keys
        for key in data:
            if key not in AVAILABLE_KEYS:
                raise errors.ValidationError(f"{tile_id} movement unknown key: '{key}'")

        return movement
