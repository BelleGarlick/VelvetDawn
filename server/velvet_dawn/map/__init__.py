import velvet_dawn
from velvet_dawn.config import Config
from velvet_dawn.dao import db
from velvet_dawn.dao.models import KeyValues, Keys, Tile , Entity
from velvet_dawn import datapacks

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
        "tiles": [
            x.json() for x in db.session.query(Tile).all()
        ]
    }


def is_placeable(x: int, y: int) -> bool:
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
    entity_at_position = db.session.query(Entity).where(Entity.pos_x == x, Entity.pos_y == y).one_or_none()
    if entity_at_position:
        return False

    db_tile = get_tile(x, y)
    if not db_tile:
        return False

    tile = datapacks.tiles[db_tile.tile_id]

    return tile.traversable


def get_tile(x, y):
    return db.session.query(Tile)\
        .where(Tile.x == x, Tile.y == y)\
        .one_or_none()
