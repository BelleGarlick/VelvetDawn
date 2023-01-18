import velvet_dawn.db.instance as db


""" Tags interface with the dao

This module stores tags in two ways, tags -> entities and
entities -> tags. This allows O(1) access for all entities
with a tag or all tags on an entities. This implementation 
detail should be abstracted from the uses of this module.

This file is structured as:
 - adding tags 
 - removing tags
 - get instances with a given tag
 - get all tags on an instance
 - check if the instance has a given tag
"""


# Store the list of instance ids for a given tag, e.g. UNITS-BY-TAG#tag:example - {1, 2, 3}
UNITS_BY_TAG_PREFIX = "UNITS-BY-TAG#{}"
TILES_BY_TAG_PREFIX = "TILES-BY-TAG#{}"

# Store the list of tags in a given instance, e.g. TAGS#units#1 - {tag:example, tag:example2}
UNIT_TAGS = "TAGS#units#{}"
TILES_TAGS = "TAGS#tiles#{}"
WORLD_TAGS = "TAGS#world"


def add_unit_tag(unit_id: str, tag: str):
    """ Add tag to unit in both places """
    # Add tag to set of tags in the unit
    db.sadd(UNIT_TAGS.format(unit_id), [tag])

    # Add unit to the set of units grouped by the tag
    db.sadd(UNITS_BY_TAG_PREFIX.format(tag), [unit_id])


def add_tile_tag(tile_id, tag):
    """ Add tag to tile in both places """
    # Add tag to set of tags in the tile
    db.sadd(TILES_TAGS.format(tile_id), [tag])

    # Add unit to the set of tiles grouped by the tag
    db.sadd(TILES_BY_TAG_PREFIX.format(tag), [tile_id])


def add_world_tag(tag):
    """ Add tag to world """
    # Add tag to set of tags in the world
    db.sadd(WORLD_TAGS, [tag])


def remove_unit_tag(unit_id: str, tag: str):
    """ Remove unit from tags in both places """
    # Add tag to set of tags in the unit
    db.srem(UNIT_TAGS.format(unit_id), [tag])

    # Add unit to the set of units grouped by the tag
    db.srem(UNITS_BY_TAG_PREFIX.format(tag), [unit_id])


def remove_tile_tag(tile_id, tag):
    """ Remove tiles from tags in both places """
    # Add tag to set of tags in the tile
    db.srem(TILES_TAGS.format(tile_id), [tag])

    # Add unit to the set of tiles grouped by the tag
    db.srem(TILES_BY_TAG_PREFIX.format(tag), [tile_id])


def remove_world_tag(tag):
    """ Remove world tags """
    # Add tag to set of tags in the world
    db.srem(WORLD_TAGS, [tag])


def get_units_with_tag(tag):
    """ Get all units with a tag """
    return db.smembers(UNITS_BY_TAG_PREFIX.format(tag))


def get_tiles_with_tag(tag):
    """ Get all tiles with a tag """
    return db.smembers(TILES_BY_TAG_PREFIX.format(tag))


def get_unit_tags(unit_id):
    """ Get all tags on a unit """
    return db.smembers(UNIT_TAGS.format(unit_id))


def get_tile_tags(tile_id):
    """ Get all tags on a tile """
    return db.smembers(TILES_TAGS.format(tile_id))


def get_world_tags():
    """ Get all tags on the world instance """
    return db.smembers(WORLD_TAGS)


def is_unit_tagged(unit_id, tag):
    """ Check if the unit has a given tag """
    return db.sismember(UNIT_TAGS.format(unit_id), tag)


def is_tile_tagged(tile_id, tag):
    """ Check if the tile has a given tag """
    return db.sismember(TILES_TAGS.format(tile_id), tag)


def is_world_tagged(tag):
    """ Check if the world has a given tag """
    return db.sismember(WORLD_TAGS, tag)


# TODO Use when a unit is killed
def remove_unit(unit_id):
    for tag in list(get_unit_tags(unit_id)):
        remove_unit_tag(unit_id, tag)
    db.rem(UNIT_TAGS.format(unit_id))
