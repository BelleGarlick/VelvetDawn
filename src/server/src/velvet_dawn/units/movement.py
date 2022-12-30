from typing import List, Dict

import velvet_dawn
from velvet_dawn import errors
from velvet_dawn.dao import db
import velvet_dawn.map.neighbours
from velvet_dawn.config import Config
from velvet_dawn.models import Phase, Coordinate
from velvet_dawn.dao.models import Player, Entity


def get_remaining_moves(entity: Entity):
    # TODO Test this when influence is done
    # TODO Add influence here and other mechanics here
    return entity.movement_remaining


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

    entity = velvet_dawn.units.get_unit_by_id(entity_pk)
    if entity is None:
        raise errors.ItemNotFoundError(entity_pk)

    if entity.player != player.name:
        raise errors.ValidationError("You may only move your own pieces.")

    # Validate correct path and calculate remaining moves
    remaining_moves = _validate_entity_traversing_path(entity, path, config)

    # Update the entity to the new position based on the path and the remaining moves
    db.session.query(Entity).where(Entity.id == entity_pk).update({
        Entity.movement_remaining: remaining_moves,
        Entity.pos_x: path[-1]['x'],
        Entity.pos_y: path[-1]['y']
    })
    db.session.commit()


def _validate_entity_traversing_path(entity: Entity, path: List[Dict[str, int]], config: Config) -> int:
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

    if tiles[0].x != entity.pos_x or tiles[0].y != entity.pos_y:
        raise errors.EntityMovementErrorInvalidStartPos()

    for i, tile in enumerate(tiles):
        if not tile:
            raise errors.EntityMovementErrorInvalidItem()

        # Check if the previous tile is a neighbour
        if i > 0 and tiles[i - 1] not in velvet_dawn.map.neighbours.get_neighbours(Coordinate(tile.x, tile.y), config):
            raise errors.EntityMovementErrorNotNeighbours(i + 1)

        # If the player already exists in this tile then we don't need to
        # check if it's valid or decrement the remaining moves
        if tile.x == entity.pos_x and tile.y == entity.pos_y:
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