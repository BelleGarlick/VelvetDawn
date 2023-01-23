import velvet_dawn.db.gateway as db
from velvet_dawn.db.instances import TileInstance


""" This interface defines the interface for
storing tiles in in-memory db. This interface
does no manage the chunk loading or infinite 
loading, just the in-memory tile store.
"""


TILES_KEY = "TILES"


def get_tile_instance_id(x: int, y: int):
    """ Tile ids are based on the ordinates """
    return f"{x}:{y}"


def set_tile(x: int, y: int, tile_id: str):
    """ Set the tile id in the db """
    tile_instance_id = get_tile_instance_id(x, y)
    db.hset(TILES_KEY, tile_instance_id, tile_id)

    return get_tile(x, y)


def get_tile(x: int, y: int):
    """ Get a specific tile """
    tile_instance_id = get_tile_instance_id(x, y)
    tile_id = db.hget(TILES_KEY, tile_instance_id)
    if tile_id:
        return TileInstance(
            tile_instance_id,
            tile_id,
            x,
            y
        )


def all():
    """ Get all tiles """
    db_tiles = db.get_value(TILES_KEY, [])
    tile_count = len(db_tiles)
    instances = [None] * tile_count  # pre-loading the array so that it's faster

    for i, key in enumerate(db_tiles):
        x, y = key.split(":")
        instances[i] = TileInstance(
            key,
            db_tiles[key],
            int(x),
            int(y)
        )

    return instances


def clear():
    """ Delete all tiles """
    db.rem(TILES_KEY)
