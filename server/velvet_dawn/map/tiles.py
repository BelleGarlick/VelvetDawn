from config import Config
from dao.initialisation import db
from dao.models import KeyValues, Keys

import os
from pathlib import Path
from typing import Dict

from velvet_dawn.models.tile import Tile


TILE_PATH = Path("../../datapacks")

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


def get():
    return tiles
    # width = db.session.query(KeyValues).where(KeyValues.key == Keys.MAP_WIDTH).one_or_none()
    # height = db.session.query(KeyValues).where(KeyValues.key == Keys.MAP_HEIGHT).one_or_none()
    # width, height = int(width.value), int(height.value)
    #
    # tiles_array = [
    #     [0 for _ in range(height)]
    #     for _ in range(width)
    # ]
    #
    # for tile in db.session.query(Tile).all():
    #     tiles_array[tile.x][tile.y] = tile.tile_id
    #
    # return tiles_array
