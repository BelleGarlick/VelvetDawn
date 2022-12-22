import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List

from config import Config
from logger import logger
from velvet_dawn.models.datapacks.entity import Entity
from velvet_dawn.models.datapacks.resource import Resource, ResourceType
from velvet_dawn.models.datapacks.taggable import Taggable
from velvet_dawn.models.datapacks.tile import Tile


""" datapacks module

This module is responsible for loading the datapacks into the game
"""


_BUILT_IN_DATAPACK_PATH = Path(__file__).parent / "built-in"
_DATAPACKS_PATH = Path(__file__).parent.parent.parent.parent / "datapacks"

_abstract_definitions: Dict[str, dict] = {}

tiles: Dict[str, Tile] = {}
entities: Dict[str, Entity] = {}
resources: Dict[str, Resource] = {}

tags: Dict[str, List[Taggable]] = {}


def init(config: Config):
    for datapack in os.listdir(_BUILT_IN_DATAPACK_PATH):
        _load_datapack(_BUILT_IN_DATAPACK_PATH / datapack)

    for datapack in config.datapacks:
        _load_datapack(_DATAPACKS_PATH / datapack)


def _load_datapack(datapack_path: Path):
    logging.info(f"Loading datapack '{datapack_path}'")
    datapack = datapack_path.stem

    if not datapack_path.exists():
        logging.error(f"Datapack '{datapack}' not found.")
        sys.exit(1)

    _load_tiles(datapack_path / 'tiles')
    _load_entities(datapack_path / 'entities')
    _load_resources(datapack_path / 'resources')


def get(id: str, entities_only=False, tiles_only=False, resources_only=False):
    if entities_only: return entities.get(id)
    if tiles_only: return tiles.get(id)
    if resources_only: return resources.get(id)

    if id in tags:return tags[id]
    if id in entities: return entities[id]
    if id in tiles: return tiles[id]
    if id in resources: return resources[id]

    return None


def _load_tiles(tiles_path):
    """ Load tiles

    This function will load tiles into the entities map

    Args:
        tiles_path: Path to the resource dir
    """
    global tiles

    datapack_tiles = _load_items_in_dir(tiles_path)
    for key in datapack_tiles:
        tile_data = datapack_tiles[key]
        tile_id = _construct_id(key, data=tile_data)

        logger.info(" - " + tile_id)

        tile = Tile.load(id=tile_id, data=_extend(tile_data))
        tiles[tile.id] = tile


def _load_entities(entities_path):
    """ Load entities

    This function will load entities into the entities map

    Args:
        entities_path: Path to the resource dir
    """
    global entities

    datapack_entities = _load_items_in_dir(entities_path)
    for key in datapack_entities:
        entity_data = datapack_entities[key]
        entity_id = _construct_id(key, data=entity_data)

        logger.info(" - " + entity_id)

        entity = Entity.load(id=entity_id, data=_extend(entity_data))
        entities[entity.id] = entity


def _load_resources(resources_path: Path):
    """ Load resources

    This function will load resources into the resources map

    Args:
        resources_path: Path to the resource dir
    """
    global resources

    if not resources_path.exists():
        return

    for file in os.listdir(resources_path):
        if file == ".DS_Store": continue

        logging.info(f" - {resources_path.parent}/{file}")
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

        resource_id = _construct_id(resource_path, include_file_type=True)
        resources[resource_id] = Resource(
            id=resource_id,
            path=resource_path,
            resource_type=resource_type
        )


def _construct_id(file_path: Path, include_file_type=False, data: dict = None) -> str:
    """ Construct the id for a file being loaded

    Args:
        file_path: Path to the file, used to construct id
        include_file_type: If true, the file type will be preserved
        data: If given, then will check to see if the file has an assigned id

    Returns:
        New id.
    """
    if data and "id" in data:
        return data['id']

    # TODO Doc + test
    file_name = file_path.stem

    if include_file_type:
        file_name = file_path.name

    if "_" in file_name[1:]:  # Check if there's a _ and it's not the first char
        return file_name.replace("_", ":")

    return f"{file_path.parent.parent.stem}:{file_name}"


def _load_items_in_dir(path: Path) -> Dict[Path, dict]:
    """ Load items from a directory.

    Abstracts entities will be added to the abstract entities dict and
    concrete entities will be returned. Abstract entities will be assigned
    and id here.

    Args:
        path: Directly to load

    Returns:
        Concrete entities
    """
    global _abstract_definitions

    data_paths = {}

    if not os.path.exists(path):
        return {}

    for file in sorted(os.listdir(path)):
        if file == ".DS_Store":
            continue

        with open(path / file) as reader:
            data = json.load(reader)

            if data.get("abstract", False):
                def_id = _construct_id(path / file, data=data)
                logger.info(f" - ~{def_id}")
                _abstract_definitions[def_id] = data
            else:
                data_paths[path / file] = data

    return data_paths


def _extend(main: dict) -> dict:
    """ Extend a given dictionary with the abstract definitions
     if the given dict has an `"extends": []` attribute

    Args:
        main: The dict to extend

    Returns:
        The extended dict
    """
    merged_dict = {}

    extensions = main.get("extends", [])
    for key in extensions:
        if key not in _abstract_definitions:
            raise Exception(f"Abstract file '{key}' not found. Please mark this file with a `'abstract': true` in the file's definition.")

        _merge_dicts(merged_dict, _abstract_definitions[key])

    _merge_dicts(merged_dict, main)

    return merged_dict


def _merge_dicts(merge_into, merge_from) -> dict:
    """ Merge the two dicts without keeping a reference, allowing
     for the data to be modified in the givens dicts without updating
     the original

    Args:
        merge_into: Dict to copy into from `merge_from`
        merge_from: The reference dict to copy data from

    Returns:
        Combinations of the two dicts
    """
    for key in merge_from:
        value = merge_from[key]

        if isinstance(value, dict):
            merged = {}
            _merge_dicts(merged, merge_into.get(key, {}))
            _merge_dicts(merged, merge_from[key])
            value = merged

        if isinstance(value, list):
            value = merge_into.get(key, []) + merge_from[key]

        merge_into[key] = value

    return merge_into
