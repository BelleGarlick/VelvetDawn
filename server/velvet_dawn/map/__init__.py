from dao.initialisation import db
from dao.models import KeyValues, Keys, Tile, Entity
from velvet_dawn.map.creation import new
from velvet_dawn.map.tiles import get_tiles, get as get_tile


def get():
    width = int(db.session.query(KeyValues).get(Keys.MAP_WIDTH).value)
    height = int(db.session.query(KeyValues).get(Keys.MAP_HEIGHT).value)

    return {
        "width": width,
        "height": height,
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
    entity_at_position = db.session.query(Entity).where(Entity.pos_x==x, Entity.pos_y==y).one_or_none()
    if entity_at_position:
        return False

    db_tile = get_tile(x, y)
    if not db_tile:
        return False

    tile = get_tiles()[db_tile.tile_id]

    return tile.traversable
