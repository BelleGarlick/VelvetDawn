import json
import time

import velvet_dawn.db.instance as db
import velvet_dawn

""" Attributes interface with the dao

This module stores the attributes per instance and the default
attributes per instance and the attribute updates. When an attribute
is updated, it's added to the updates list which, when loaded, removes
stale items so users don't keep loading attribute changes.

This file is structured as:
 - load and register the update changes
 - set attributes
 - reset attributes
 - get attributes
"""


# if updates are older than five seconds
#  don't broadcast to clients and remove from update cache
STALE_AGE = 5

# DB Keys
ATTRIBUTES_UPDATES = "ATTRIBUTES#updates"

UNIT_ATTRIBUTES = "ATTRIBUTES#units#{}"
UNIT_ATTRIBUTES_DEFAULTS = "ATTRIBUTES#units#{}#default"

TILES_ATTRIBUTES = "ATTRIBUTES#tiles#{}"
TILES_ATTRIBUTES_DEFAULTS = "ATTRIBUTES#tiles#{}#default"

WORLD_ATTRIBUTES = "ATTRIBUTES#world"
WORLD_ATTRIBUTES_DEFAULTS = "ATTRIBUTES#world#default"


def get_attribute_updates():
    """ Load all attribute updates and find then filter any stale updates """
    valid_items = []
    stale_items = []

    min_stale_age = time.time() - STALE_AGE

    # Loop through all items and filter if it's stale or not
    for item in db.smembers(ATTRIBUTES_UPDATES):
        parsed_item = json.loads(item)
        if parsed_item.get("time", 0) > min_stale_age:
            valid_items.append(parsed_item)
        else:
            stale_items.append(item)

    # Remove stale items
    for item in stale_items:
        db.srem(ATTRIBUTES_UPDATES, [item])

    return sorted(valid_items, key=lambda x: x['time'])


def _register_changed_attribute(instance_type: str, instance_id: str, attribute: str, value, timestamp=None):
    """ Add data to the set of updated attributes in the db set """
    if timestamp is None:
        timestamp = time.time()

    db.sadd(ATTRIBUTES_UPDATES, [json.dumps({
        "type": instance_type,
        "id": instance_id,
        "attribute": attribute,
        "value": value,
        "time": timestamp
    })])


def set_unit_attribute(unit_id, attribute: str, value):
    """ Set a unit and default attribute """
    db.hset(UNIT_ATTRIBUTES.format(unit_id), attribute, value)

    if not db.hexists(UNIT_ATTRIBUTES_DEFAULTS.format(unit_id), attribute):
        db.hset(UNIT_ATTRIBUTES_DEFAULTS.format(unit_id), attribute, value)

    _register_changed_attribute("unit", unit_id, attribute, value)


def set_tile_attribute(tile_id, attribute: str, value):
    """ Set a tile and default attribute """
    db.hset(TILES_ATTRIBUTES.format(tile_id), attribute, value)

    if not db.hexists(TILES_ATTRIBUTES_DEFAULTS.format(tile_id), attribute):
        db.hset(TILES_ATTRIBUTES_DEFAULTS.format(tile_id), attribute, value)

    _register_changed_attribute("tile", tile_id, attribute, value)


def set_world_attribute(attribute: str, value):
    """ Set a world and default attribute """
    db.hset(WORLD_ATTRIBUTES, attribute, value)

    if not db.hexists(WORLD_ATTRIBUTES_DEFAULTS, attribute):
        db.hset(WORLD_ATTRIBUTES_DEFAULTS, attribute, value)

    _register_changed_attribute("world", "world", attribute, value)


def reset_unit_attribute(unit_id, attribute: str, value):
    """ Reset a unit attribute to default value, if no default, set to given value """
    if db.hexists(UNIT_ATTRIBUTES_DEFAULTS.format(unit_id), attribute):
        set_unit_attribute(unit_id, attribute, db.hget(UNIT_ATTRIBUTES_DEFAULTS.format(unit_id), attribute))
    else:
        set_unit_attribute(unit_id, attribute, value)


def reset_tile_attribute(tile_id, attribute: str, value):
    """ Reset a tile attribute to default value, if no default, set to given value """
    if db.hexists(TILES_ATTRIBUTES_DEFAULTS.format(tile_id), attribute):
        set_tile_attribute(tile_id, attribute, db.hget(TILES_ATTRIBUTES_DEFAULTS.format(tile_id), attribute))
    else:
        set_tile_attribute(tile_id, attribute, value)


def reset_world_attribute(attribute: str, value):
    """ Reset a world attribute to default value, if no default, set to given value """
    if db.hexists(WORLD_ATTRIBUTES_DEFAULTS, attribute):
        set_world_attribute(attribute, db.hget(WORLD_ATTRIBUTES_DEFAULTS, attribute))
    else:
        set_world_attribute(attribute, value)


def get_unit_attribute(unit_id, attribute, default=None):
    """ Get a specific attribute from a unit """
    return db.hget(UNIT_ATTRIBUTES.format(unit_id), attribute, default=default)


def get_tile_attribute(tile_id, attribute, default=None):
    """ Get a specific attribute from a tile """
    return db.hget(TILES_ATTRIBUTES.format(tile_id), attribute, default=default)


def get_world_attribute(attribute, default=None):
    """ Get a specific attribute from the world """
    return db.hget(WORLD_ATTRIBUTES, attribute, default=default)


def remove_unit(unit_id):
    """ Remove all attributes from units """
    db.rem(UNIT_ATTRIBUTES.format(unit_id))
    db.rem(UNIT_ATTRIBUTES_DEFAULTS.format(unit_id))


def get_full_attribute_list():
    """ Get all attributes """
    attributes = []

    world_attributes = db.hgetall(WORLD_ATTRIBUTES)
    for key in world_attributes:
        attributes.append({
            "type": "world",
            "id": "world",
            "attribute": key,
            "value": world_attributes[key]
        })

    units = velvet_dawn.units.list()
    for unit in units:
        unit_attributes = db.hgetall(UNIT_ATTRIBUTES.format(unit.id))
        for key in unit_attributes:
            attributes.append({
                "type": "unit",
                "id": unit.id,
                "attribute": key,
                "value": unit_attributes[key]
            })

    tiles = velvet_dawn.map.list_tiles()
    for tile in tiles:
        tiles_attributes = db.hgetall(TILES_ATTRIBUTES.format(tile.id))
        for key in tiles_attributes:
            attributes.append({
                "type": "tile",
                "id": tile.id,
                "attribute": key,
                "value": tiles_attributes[key]
            })

    return attributes
