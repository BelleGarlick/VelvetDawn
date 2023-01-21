from typing import List, Dict

import velvet_dawn
from velvet_dawn import errors
import velvet_dawn.map.neighbours
from velvet_dawn.config import Config
from velvet_dawn.dao import db
from velvet_dawn.db.instances import UnitInstance
from velvet_dawn.models.phase import Phase
from velvet_dawn.models.coordinate import Coordinate
from velvet_dawn.dao.models import Player, TileInstance


def get_remaining_moves(unit: UnitInstance):
    # TODO Test this when influence is done
    # TODO Add influence here and other mechanics here
    return unit.get_attribute("movement.remaining", default=0)


def move(player: Player, entity_pk: int, path: List[dict], config: Config):
    """ Move an entity through a path

    Args:
        player: The player moving the entity
        entity_pk: The db instance id of the entity
        path: List of {x, y} positions the entity moves, starting with it's current pos
        config: The came config
    """
    if velvet_dawn.game.phase.get_phase() != Phase.GAME:
        raise errors.GamePhaseError("game")

    if velvet_dawn.game.turns.get_active_turn(Phase.GAME) != player.team:
        raise errors.InvalidTurnError()

    entity = velvet_dawn.db.units.get_unit_by_instance_id(entity_pk)
    if entity is None:
        raise errors.ItemNotFoundError(entity_pk)

    if entity.player != player.name:
        raise errors.ValidationError("You may only move your own pieces.")

    # Validate correct path and calculate remaining moves
    remaining_moves = _validate_entity_traversing_path(entity, path, config)

    # Run leave movement triggers
    trigger_on_leave_actions(entity, velvet_dawn.map.get_tile(entity.x, entity.y))

    # Update the entity to the new position based on the path and the remaining moves
    entity.set_attribute("movement.remaining", remaining_moves)
    instance = velvet_dawn.db.units.move(entity, path[-1]['x'], path[-1]['y'])
    db.session.commit()

    # Run enter movement triggers
    trigger_on_enter_actions(
        instance,
        velvet_dawn.map.get_tile(instance.tile_x, instance.tile_y)
    )

    return instance


def _validate_entity_traversing_path(entity: UnitInstance, path: List[Dict[str, int]], config: Config) -> int:
    """ Validate an entity's traversal path

    This function will raise exceptions if the path is invalid.

    Args:
        entity: The entity to move
        path: The list of {x: , y: } point the entity traverses

    Returns:
        Number of remaining moves the entity has

    Raises:
        Exception if the path is invalid
    """
    tiles = [velvet_dawn.map.get_tile(point['x'], point['y']) for point in path]
    remaining_moves = get_remaining_moves(entity)

    if tiles[0].x != entity.x or tiles[0].y != entity.y:
        raise errors.EntityMovementErrorInvalidStartPos()

    for i, tile in enumerate(tiles):
        if not tile:
            raise errors.EntityMovementErrorInvalidItem()

        # Check if the previous tile is a neighbour
        if i > 0 and tiles[i - 1] not in velvet_dawn.map.neighbours.get_neighbours(Coordinate(tile.x, tile.y), config):
            raise errors.EntityMovementErrorNotNeighbours(i + 1)

        # If the player already exists in this tile then we don't need to
        # check if it's valid or decrement the remaining moves
        if tile.x == entity.x and tile.y == entity.y:
            continue

        tile_definition = velvet_dawn.datapacks.tiles.get(tile.tile_id)
        if not tile_definition:
            raise errors.UnknownTile(tile.tile_id)

        if not velvet_dawn.map.is_traversable(tile.x, tile.y):
            raise errors.EntityMovementErrorTileNotTraversable(tile)

        if remaining_moves <= 0:
            raise errors.EntityMovementErrorTileNoRemainingMoves()

        remaining_moves -= velvet_dawn.map.get_tile_movement_weight(tile)

    return remaining_moves


def trigger_on_leave_actions(unit_instance: UnitInstance, tile_instance: TileInstance):
    """ Trigger on leave actions

    This occurs when an entity leaves a tile, both the tile and
    unit will be called here

    This function is testing as part of the trigger testing suite
    not movement suite

    Args:
        unit_instance: The unit to trigger on
        tile_instance: The tile to trigger on
    """
    velvet_dawn.datapacks.entities[unit_instance.entity_id].triggers.on_leave(unit_instance)
    velvet_dawn.datapacks.tiles[tile_instance.tile_id].triggers.on_leave(tile_instance)


def trigger_on_enter_actions(unit_instance: UnitInstance, tile_instance: TileInstance):
    """ Trigger on enter actions

    This occurs when an entity enters a tile, both the tile and
    unit will be called here

    This function is testing as part of the trigger testing suite
    not movement suite

    Args:
        unit_instance: The unit to trigger on
        tile_instance: The tile to trigger on
    """
    velvet_dawn.datapacks.entities[unit_instance.entity_id].triggers.on_enter(unit_instance)
    velvet_dawn.datapacks.tiles[tile_instance.tile_id].triggers.on_enter(tile_instance)
