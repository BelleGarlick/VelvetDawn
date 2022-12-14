from config import Config
from dao.initialisation import db
from dao.models import KeyValues, Keys, Tile as DbTile

import os
from pathlib import Path
from typing import Dict

from velvet_dawn.models.tile import Tile


TILE_PATH = Path(__file__).parent.parent.parent.parent / "datapacks"

tiles: Dict[str, Tile] = {}


def initialise(config: Config):
    print("Initialising Tiles")
    global tiles

    if not TILE_PATH.exists():
        raise Exception("data/tiles does not exist")

    tiles = {}
    for datapack in config.datapacks:
        tile_path = TILE_PATH / datapack / 'tiles'
        if not tile_path.exists():
            continue

        tile_files = os.listdir(tile_path)

        for file in tile_files:
            print(f" - {datapack}/{file}")
            tile = Tile.load(tile_path / file)
            tiles[tile.id] = tile


def get_tiles() -> Dict[str, Tile]:
    return tiles


def get(x, y):
    return db.session.query(DbTile)\
        .where(DbTile.x == x, DbTile.y == y)\
        .one_or_none()
