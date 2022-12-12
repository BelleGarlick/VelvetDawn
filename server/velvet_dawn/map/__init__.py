from dao.initialisation import db
from dao.models import KeyValues, Keys, Tile
from velvet_dawn.map.creation import new
from velvet_dawn.map.tiles import get_tiles


def get():
    width, height = int(KeyValues.get(Keys.MAP_WIDTH)), int(KeyValues.get(Keys.MAP_HEIGHT))
    return {
        "width": width,
        "height": height,
        "tiles": [x.json() for x in get_tiles().values()],
        "layout": [
            [
                db.session.query(Tile).query(Tile.x == c, Tile.y == r).one_or_none().json()
                for r in range(height)
            ]
            for c in range(width)
        ]
    }
