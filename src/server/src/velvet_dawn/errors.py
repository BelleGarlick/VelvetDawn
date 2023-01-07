

class ValidationError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class UnknownEntityError(ValidationError):
    def __init__(self, entity: str):
        ValidationError.__init__(self, f"Unknown entity id '{entity}'")


class EntityMissingFromSetupDefinition(ValidationError):
    def __init__(self, entity):
        ValidationError.__init__(self, f"Entity missing from setup definition '{entity}'")


class EntityMovementErrorInvalidStartPos(ValidationError):
    def __init__(self):
        ValidationError.__init__(self, "The first element of the paths must be the entities position")


class EntityMovementErrorInvalidItem(ValidationError):
    def __init__(self):
        ValidationError.__init__(self, "Tile in path sequence is in invalid.")


class EntityMovementErrorNotNeighbours(ValidationError):
    def __init__(self, i):
        ValidationError.__init__(self, f"All tiles must be neighbours. Tile {i - 1} is not a neighbour of tile {i}.")


class UnknownTile(ValidationError):
    def __init__(self, tile_id):
        ValidationError.__init__(self, f"Unknown Tile '{tile_id}'")


class EntityMovementErrorTileNotTraversable(ValidationError):
    def __init__(self, tile):
        ValidationError.__init__(self, f"Tile ({tile.x}, {tile.y}) is not traversable")


class EntityMovementErrorTileNoRemainingMoves(ValidationError):
    def __init__(self):
        ValidationError.__init__(self, f"Unit has no further remaining moves to spend")


class GamePhaseError(ValidationError):
    def __init__(self, phase):
        ValidationError.__init__(self, f"You may only perform this action during the {phase} phase of the game.")


class InvalidTurnError(ValidationError):
    def __init__(self):
        ValidationError.__init__(self, "You may only perform this error during your turn.")


class ItemNotFoundError(ValidationError):
    def __init__(self, item_id):
        ValidationError.__init__(self, f"Item not found '{item_id}'")
