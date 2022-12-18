import logging
import os
import sys
from pathlib import Path
from typing import Dict

from config import Config
from velvet_dawn.models.entity import Entity
from velvet_dawn.models.resource import Resource, ResourceType
from velvet_dawn.models.tile import Tile

_DATAPACKS_PATH = Path(__file__).parent.parent.parent.parent / "datapacks"


tiles: Dict[str, Tile] = {}
entities: Dict[str, Entity] = {}
resources: Dict[str, Resource] = {}


def init(config: Config):
    for datapack in config.datapacks:
        datapack_path = _DATAPACKS_PATH / datapack
        logging.info(f"Loading datapack '{datapack_path}'")

        if not datapack_path.exists():
            logging.error(f"Datapack '{datapack}' not found.")
            sys.exit(1)

        _load_tiles(datapack, datapack_path / 'tiles')
        _load_entities(datapack, datapack_path / 'entities')
        _load_resources(datapack, datapack_path / 'resources')


def _load_tiles(datapack, tiles_path):
    global tiles

    if not tiles_path.exists():
        return

    for file in os.listdir(tiles_path):
        if file == ".DS_Store": continue

        logging.info(f" - {datapack}/{file}")
        tile = Tile.load(tiles_path / file)
        tiles[tile.id] = tile


def _load_entities(datapack, entities_path):
    global entities

    if not entities_path.exists():
        return

    for file in os.listdir(entities_path):
        if file == ".DS_Store": continue

        logging.info(f" - {datapack}/{file}")
        entity = Entity.load(entities_path / file)
        entities[entity.id] = entity


def _load_resources(datapack, resources_path):
    global resources

    if not resources_path.exists():
        return

    for file in os.listdir(resources_path):
        if file == ".DS_Store": continue

        logging.info(f" - {datapack}/{file}")
        resource_path = resources_path / file

        file_type, resource_type = resource_path.suffix[1:], ResourceType.Audio
        if file_type in {"mp3"}:
            resource_type = ResourceType.Audio
        elif file_type in {"woff"}:
            resource_type = ResourceType.Font
        elif file_type in {"jpg", "png"}:
            resource_type = ResourceType.Image
        else:
            raise Exception(f"Resource '{resource_path}' is invalid. File types may only be mp3, woff, jpg or png")

        resource_id = f"{datapack}:{file}"
        resources[resource_id] = Resource(
            id=resource_id,
            path=resource_path,
            resource_type=resource_type
        )