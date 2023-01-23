import math

import velvet_dawn
from velvet_dawn.config import Config
from velvet_dawn.dao import db
from velvet_dawn.dao.models import KeyValues, Keys
from velvet_dawn.db.instances import TileInstance

from velvet_dawn.map.creation import new
from velvet_dawn.map.spawn import allocate_spawn_points, get_allocated_spawn_area, is_point_spawnable


def get(config: Config):
    width = db.session.query(KeyValues).get(Keys.MAP_WIDTH)
    height = db.session.query(KeyValues).get(Keys.MAP_HEIGHT)

    map_side_invalid = False
    if not (width and height):
        map_side_invalid = True

    elif int(width.value) != config.map_width and int(height.value) != config.map_height:
        map_side_invalid = True

    if map_side_invalid:
        velvet_dawn.map.new(config)

    return {
        "width": config.map_width,
        "height": config.map_height,
        "tiles": [x.json() for x in velvet_dawn.db.tiles.all()]
    }


def is_traversable(x: int, y: int) -> bool:
    """ Check if a tile can have an entity placed in it
    or traversed through it.

    First we check if there's already an entity at that
    position, then we try to get the tile at that pos
    then check if it's traversable.

    Args:
        x: X ordinate of the tile
        y: Y ordinate of the tile

    Returns:
        If the tile is traversable
    """
    # First check if there is already an entity at that position
    if velvet_dawn.db.units.get_units_at_positions(x, y):
        return False

    db_tile = velvet_dawn.db.tiles.get_tile(x, y)
    if not db_tile:
        return False

    return db_tile.get_attribute("movement.traversable", default=True)


def get_tile_movement_weight(tile: TileInstance):
    # TODO Incorporate influence or changes
    return tile.get_attribute("movement.weight")


def get_distance(origin, to):
    """ Calculate the distance between two positions. This function
    is designed for flat-top hexagons where the second column
    is sunk vertically. Changes to that layout will require changes
    to this function.

    This function is also implemented in the FE for
    combat and targeting.

    Args:
        origin: Point a
        to: Point b

    Returns:
        Int distance between
    """
    dcol = abs(origin.x - to.x)
    drow = abs(origin.y - to.y)

    distance = max(dcol, drow + dcol / 2)

    if origin.x % 2 == 0 and dcol % 2 == 1:
        if to.y <= origin.y:
            return math.floor(distance)
        return math.ceil(distance)

    elif dcol % 2 == 1:
        if to.y <= origin.y:
            return math.ceil(distance)
        return math.floor(distance)

    return int(distance)
