import copy
import json
import logging
import os
from pathlib import Path
from typing import Dict, List

from velvet_dawn import errors
from velvet_dawn.config import Config
from velvet_dawn.logger import logger
from velvet_dawn.models.datapacks.units.unit import Unit
from velvet_dawn.models.datapacks.resource import Resource, ResourceType
from velvet_dawn.models.datapacks.tiles.tile import Tile
from velvet_dawn.models.datapacks.world import WorldDefinition

""" datapacks module

This module is responsible for loading the datapacks into the game
and assigning all the ids.
"""


_BUILT_IN_DATAPACK_PATH = Path(__file__).parent / "built-in"
_DATAPACKS_PATH = Path(__file__).parent.parent.parent.parent.parent.parent / "datapacks"

_abstract_definitions: Dict[str, dict] = {}

world = WorldDefinition()
tiles: Dict[str, Tile] = {}
entities: Dict[str, Unit] = {}
resources: Dict[str, Resource] = {}


def init(config: Config):
    # TODO Test that testing pack will load
    _load_datapack(_BUILT_IN_DATAPACK_PATH / "base")

    if "__testing__" in config.datapacks:
        _load_datapack(_BUILT_IN_DATAPACK_PATH / "__testing__")
        config.datapacks.remove("__testing__")

    for datapack in config.datapacks:
        _load_datapack(_DATAPACKS_PATH / datapack)


def _load_datapack(datapack_path: Path):
    logging.info(f"Loading datapack '{datapack_path}'")
    datapack = datapack_path.stem

    if not datapack_path.exists():
        raise errors.ValidationError(f"Datapack '{datapack}' not found.")

    datapack_id = _load_datapack_metadata(datapack_path)

    _load_resources(datapack_path / 'resources', datapack_id)
    _load_tiles(datapack_path / 'tiles', datapack_id)
    _load_entities(datapack_path / 'entities', datapack_id)


def _load_datapack_metadata(datapack_path: Path):
    path = datapack_path / 'datapack.json'
    base_id = datapack_path.stem
    if not path.exists():
        return base_id

    with open(path) as file:
        data = json.load(file)
        id = data.get("id", base_id)

        WorldDefinition().load(id, data)

        return id


def _load_tiles(tiles_path, datapack_id):
    """ Load tiles

    This function will load tiles into the entities map

    Args:
        tiles_path: Path to the resource dir
        datapack_id: The datapack id
    """
    global tiles

    datapack_tiles = _load_items_in_dir(tiles_path, datapack_id)
    for key in datapack_tiles:
        tile_data = datapack_tiles[key]
        tile_id = _construct_id(datapack_id, tiles_path, key, data=tile_data)

        logger.info(" - " + tile_id)

        tile = Tile.load(tile_id=tile_id, data=_extend(tile_data))
        tiles[tile.id] = tile


def _load_entities(entities_path, datapack_id):
    """ Load entities

    This function will load entities into the entities map

    Args:
        entities_path: Path to the resource dir
        datapack_id: The datapack id
    """
    global entities

    datapack_entities = _load_items_in_dir(entities_path, datapack_id)
    for key in datapack_entities:
        entity_data = datapack_entities[key]
        entity_id = _construct_id(datapack_id, entities_path, key, data=entity_data)

        logger.info(" - " + entity_id)

        entity = Unit.load(parent_id=entity_id, data=_extend(entity_data))
        entities[entity.id] = entity


# TODO Test overriding
def _load_resources(resources_path: Path, datapack_id: str):
    """ Load resources

    This function will load resources into the resources map

    Args:
        resources_path: Path to the resource dir
        datapack_id: The datapack prefix
    """
    global resources

    overrides = {}

    for resource_path in _scan_dir(resources_path):
        if resource_path.name == "overrides.json":
            with open(resource_path.name) as reader:
                overrides = json.load(reader)
            continue

        resource_id = _construct_id(datapack_id, resources_path, resource_path, include_file_type=True)
        logging.info(f" - {resource_id}")

        file_type, resource_type = resource_path.suffix[1:], ResourceType.Audio
        if file_type in {"mp3"}:
            resource_type = ResourceType.Audio
        elif file_type in {"woff"}:
            resource_type = ResourceType.Font
        elif file_type in {"jpg", "png", "svg"}:
            resource_type = ResourceType.Image
        else:
            raise Exception(f"Resource '{resource_path}' is invalid. File types may only be mp3, woff, jpg or png or 'overrides.json'")

        # Override the resource from the overrides if it exists, otherwise, use the resource id
        resource_id = overrides.get(resource_id, resource_id)
        resources[resource_id] = Resource(
            id=resource_id,
            path=resource_path,
            resource_type=resource_type
        )


def _construct_id(datapack_id: str, loader_dir_path: Path, file_path: Path, include_file_type=False, data: dict = None) -> str:
    """ Construct the id for a file being loaded

    Args:
        datapack_id: The id of the datapack being loaded
        loader_dir_path: The root path where files are loaded from within.
            This should be the path to the entities, tiles or resources
        file_path: Path to the file, used to construct id
        include_file_type: If true, the file type will be preserved
        data: If given, then will check to see if the file has an assigned id

    Returns:
        New id.
    """
    if data and "id" in data:
        return data['id']

    # Get just the tokens within the loader_dir_path.
    file_parts = list(file_path.parts)[len(list(loader_dir_path.parts)):]

    if not include_file_type:
        file_parts[-1] = file_path.stem

    return datapack_id + ":" + ".".join(file_parts)


def _load_items_in_dir(root_path: Path, datapack_id: str) -> Dict[Path, dict]:
    """ Load items from a directory.

    Abstracts entities will be added to the abstract entities dict and
    concrete entities will be returned. Abstract entities will be assigned
    and id here.

    Args:
        root_path: Directly to load
        datapack_id: The datapack id

    Returns:
        Concrete entities
    """
    global _abstract_definitions

    data_paths = {}

    for file_path in sorted(_scan_dir(root_path)):
        with open(file_path) as reader:
            try:
                data = json.load(reader)
            except Exception as e:
                logger.error(e)
                raise errors.ValidationError(f"Unable to parse file: {file_path}")

            if data.get("abstract", False):
                def_id = _construct_id(datapack_id, root_path, file_path, data=data)
                logger.info(f" - ~{def_id}")
                _abstract_definitions[def_id] = data
            else:
                data_paths[file_path] = data

    return data_paths


def _scan_dir(dir: Path) -> List[Path]:
    """ Scan directory

    Walk the tree if directories listing all files within.

    Args:
        dir: top level to scan
    """
    if not os.path.exists(dir):
        return []

    found_files = []

    paths = [dir]
    while paths:
        current_path = paths.pop(0)

        for file in os.listdir(current_path):
            if file == ".DS_Store":
                continue

            file_path = current_path / file
            if file_path.is_dir():
                paths.append(file_path)
            else:
                found_files.append(file_path)

    return found_files


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

        _merge_dicts(merged_dict, copy.deepcopy(_abstract_definitions[key]))

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
