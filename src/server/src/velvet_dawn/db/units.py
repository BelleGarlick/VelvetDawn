import json
import time
import uuid
from typing import Optional, List

import velvet_dawn.db.instance as db
import velvet_dawn.models
from velvet_dawn import errors
from velvet_dawn.db.instances import UnitInstance

""" Units interface for interacting with the various
unit caches.

This module does not 

There is a lot of duplication here, but this is to enable 
O(1) access for all attributes. This means each unit is stored
in duplicated indexes but because everything is O(1) speed is
minimally impacted.
"""


# Broadcast updates for five seconds
BROADCAST_TIME = 5

# DB Keys
ALL_UNITS = "UNITS"
UNIT_UPDATES_UPDATED = "UNIT#updates#updated"
UNIT_UPDATES_REMOVED = "UNIT#updates#removed"
UNITS_CHANGES = "UNITS#changes"
UNITS_BY_PLAYER = "UNITS#players#{}"
UNITS_BY_POSITION = "UNITS#position#{}-{}"
UNITS_BY_ID = "UNITS#unit-id#{}"


def _create_unit_data(unit_id: str, player_name: str, x: float, y: float) -> dict:
    """ Create the unit instance data """
    return {
        "instance_id": str(uuid.uuid4()),
        "id": unit_id,
        "player": player_name,
        "position": {
            "x": x,
            "y": y
        }
    }


def get_updates():
    """ Get all unit updates within the last five sections and clean
     up stale items
    """
    valid_update_items, stale_update_items = [], []
    valid_removed_items, stale_removed_items = [], []

    min_stale_age = time.time() - BROADCAST_TIME

    for item in db.smembers(UNIT_UPDATES_UPDATED):
        parsed_item = json.loads(item)
        if parsed_item.get("time", 0) > min_stale_age:
            valid_update_items.append(parsed_item)
        else:
            stale_update_items.append(item)

    for item in db.smembers(UNIT_UPDATES_REMOVED):
        parsed_item = json.loads(item)
        if parsed_item.get("time", 0) > min_stale_age:
            valid_removed_items.append(parsed_item)
        else:
            stale_removed_items.append(item)

    # Remove stale items
    for item in stale_update_items:
        db.srem(UNIT_UPDATES_UPDATED, [item])
    for item in stale_removed_items:
        db.srem(UNIT_UPDATES_REMOVED, [item])

    return {
        "updates": sorted(valid_update_items, key=lambda x: x['time']),
        "removed": sorted(valid_removed_items, key=lambda x: x['time'])
    }


def spawn(unit_def, player_name: str, x: float, y: float) -> UnitInstance:
    """ Spawn a unit """
    data = _create_unit_data(unit_def.id, player_name, x, y)
    string_data = json.dumps(data)
    instance = UnitInstance(data)

    # Update the various indexes
    db.hset(ALL_UNITS, instance.instance_id, string_data)
    db.hset(UNITS_BY_PLAYER.format(player_name), instance.instance_id, string_data)
    db.hset(UNITS_BY_POSITION.format(instance.tile_x, instance.tile_y), instance.instance_id, string_data)
    db.hset(UNITS_BY_ID.format(unit_def.id), instance.instance_id, string_data)

    # Attributes and tags
    unit_def.attributes.save_to_db(instance)
    unit_def.tags.save_to_db(instance)

    # Trigger on spawn
    unit_def.triggers.on_spawn(instance)

    # Add to updates
    submission_data = instance.json()
    submission_data['time'] = time.time()
    db.sadd(UNIT_UPDATES_UPDATED, [json.dumps(submission_data)])

    return instance


def move(instance: UnitInstance, x: float, y: float) -> UnitInstance:
    """ Move a unit """
    current_instance = get_unit_by_instance_id(instance.instance_id)
    if current_instance:
        # If same, return self
        if current_instance.x == x and current_instance.y == y:
            return current_instance

        db.hdel(
            UNITS_BY_POSITION.format(current_instance.tile_x, current_instance.tile_y),
            current_instance.instance_id
        )

        current_instance.data['position']['x'] = x
        current_instance.data['position']['y'] = y

        string_data = json.dumps(current_instance.data)
        db.hset(ALL_UNITS, current_instance.instance_id, string_data)
        db.hset(UNITS_BY_PLAYER.format(current_instance.player), current_instance.instance_id, string_data)
        db.hset(UNITS_BY_POSITION.format(current_instance.tile_x, current_instance.tile_y), current_instance.instance_id, string_data)
        db.hset(UNITS_BY_ID.format(current_instance.entity_id), current_instance.instance_id, string_data)

        # Add updates
        submission_data = current_instance.json()
        submission_data['time'] = time.time()
        db.sadd(UNIT_UPDATES_UPDATED, [json.dumps(submission_data)])

        return current_instance
    else:
        raise errors.ValidationError("Given instance is out of date and does not exist at this position.")


def remove(instance: UnitInstance):
    """ Remove a specific unit from all indexes and tags/attributes """
    # Remove from indexes
    current_instance = get_unit_by_instance_id(instance.instance_id)
    if current_instance:
        db.hdel(ALL_UNITS, current_instance.instance_id)
        db.hdel(UNITS_BY_PLAYER.format(current_instance.player), current_instance.instance_id)
        db.hdel(UNITS_BY_POSITION.format(current_instance.tile_x, current_instance.tile_y), current_instance.instance_id)
        db.hdel(UNITS_BY_ID.format(current_instance.entity_id), current_instance.instance_id)

        # Add to removed
        current_instance.data['time'] = time.time()
        db.sadd(UNIT_UPDATES_REMOVED, [json.dumps(current_instance.data)])

        # Remove tags
        velvet_dawn.db.tags.remove_unit(current_instance.instance_id)
        velvet_dawn.db.attributes.remove_unit(current_instance.instance_id)


def get_all_units() -> List[UnitInstance]:
    """ Get all units """
    return [UnitInstance(json.loads(x)) for x in db.hvals(ALL_UNITS)]


def get_all_player_units(player: str) -> List[UnitInstance]:
    """ Get all units owned by a player """
    return [UnitInstance(json.loads(x)) for x in db.hvals(UNITS_BY_PLAYER.format(player))]


def get_units_at_positions(x: int, y: int) -> List[UnitInstance]:
    """ Get units at position """
    return [UnitInstance(json.loads(x)) for x in db.hvals(UNITS_BY_POSITION.format(
        x, y
    ))]


def get_units_by_unit_id(unit_id: str) -> List[UnitInstance]:
    """ Get units by unit id """
    return [UnitInstance(json.loads(x)) for x in db.hvals(UNITS_BY_ID.format(unit_id))]


def get_unit_by_instance_id(instance_id: str) -> Optional[UnitInstance]:
    """ Get the unit with a specific instance """
    data = db.hget(ALL_UNITS, instance_id)
    if data:
        return UnitInstance(json.loads(data))
