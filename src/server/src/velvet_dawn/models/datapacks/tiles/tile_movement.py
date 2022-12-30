from velvet_dawn import errors


# TODO Test and document
# Test all permiatations and erronous keys


""" Tile Movement

Defines the movement data for a tile. 
For now the only attributes are penalty and transferability,
which by default is 1. Higher penalties will take up higher
amounts of unit movement bandwidth 
"""


AVAILABLE_KEYS = {"penalty", "traversable", "notes"}


class TileMovement:
    def __init__(self):
        self.penalty: int = 1
        self.traversable = True

    def json(self):
        return {
            "penalty": self.penalty,
            "traversable": self.traversable
        }

    @staticmethod
    def load(tile_id: str, data: dict):
        """ Parse the movement data for a tile """
        movement = TileMovement()

        movement.penalty = data.get("penalty", 1)
        movement.traversable = data.get("traversable", True)

        if not isinstance(movement.penalty, int):
            raise errors.ValidationError(f"{tile_id} movement penalty must be a number.")
        if movement.penalty < 1:
            raise errors.ValidationError(f"{tile_id} movement penalty must be at least 1.")

        if not isinstance(movement.traversable, bool):
            raise errors.ValidationError(f"{tile_id} movement transferability must be either true or false.")

        # Check for random other keys
        for key in data:
            if key not in AVAILABLE_KEYS:
                raise errors.ValidationError(f"{tile_id} movement unknown key: '{key}'")

        return movement
