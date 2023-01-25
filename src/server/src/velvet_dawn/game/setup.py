from typing import List

import velvet_dawn
from velvet_dawn import datapacks, errors
from velvet_dawn.db.instances import UnitInstance
from velvet_dawn.db.models import Phase
from velvet_dawn.models.coordinate import Coordinate
from velvet_dawn.models.game_setup import GameSetup


""" velvet_dawn.game.setup

This module handles the entity setup for the games. There
are functions for the admin to control the number of units
each player gets and if it's valid to start the game.

This module also contains functions for the player to place 
their initial setup entities when in the setup phase.
"""


def get_setup(player: str):
    """ Get the game setup definition """
    entity_setup_map = velvet_dawn.db.setup_untits.get()

    commander_entities = {
        entity_id
        for entity_id in entity_setup_map
        if datapacks.entities[entity_id].commander and entity_setup_map[entity_id] > 0
    }

    units = {
        entity_id: entity_setup_map[entity_id] for entity_id in entity_setup_map
        if not datapacks.entities[entity_id].commander and entity_setup_map[entity_id] > 0
    }

    # calculate remaining players
    placed_commander, remaining_units = False, {x: units[x] for x in units}
    player_entities = velvet_dawn.db.units.get_all_player_units(player)
    for entity in player_entities:
        if entity.entity_id in commander_entities:
            placed_commander = True
        else:
            remaining_units[entity.entity_id] -= 1

    return GameSetup(
        commanders=commander_entities,
        units=units,
        placed_commander=placed_commander,
        remaining_units=remaining_units
    )


def update_setup(entity_id: str, count: int):
    """ Update the initial entities a player may use

    Args:
        entity_id: The id to update the count for
        count: Number of items the user can start with
            If the entity is a commaner then this will
            be ignored.
    """
    if velvet_dawn.db.key_values.get_phase() != Phase.Lobby:
        raise errors.ValidationError("Game setup units may only be changed in the lobby by the admin")

    # Check entity exists
    if entity_id not in datapacks.entities:
        raise errors.ValidationError(f"Unknown entity id: '{entity_id}'")

    velvet_dawn.db.setup_untits.set_count(entity_id, count)


def is_setup_valid(player):
    """ Setup definitions must contain commanders """
    return bool(get_setup(player).commanders)


def place_entity(player: str, entity_id: str, x: int, y: int):
    if velvet_dawn.db.key_values.get_phase() != Phase.Setup:
        raise errors.ValidationError("Game setup may only be changed during game setup")

    setup = get_setup(player)

    if entity_id not in datapacks.entities:
        raise errors.UnknownEntityError(entity_id)

    if not velvet_dawn.map.is_point_spawnable(user=player, x=x, y=y):
        raise errors.ValidationError("This point is not within your spawn territory")

    if not velvet_dawn.map.is_traversable(x=x, y=y):
        raise errors.ValidationError("Unit cannot be placed here.")

    # Check that the entity is valid within the setup definition
    if entity_id in setup.commanders:
        # Check they don't already have a commander
        if setup.placed_commander:
            raise errors.ValidationError("You already have a commander in play")
    else:
        remaining_units = setup.remaining_units.get(entity_id, None)
        if remaining_units is None:
            raise errors.EntityMissingFromSetupDefinition(f"Enitity {entity_id} not included in the setup definition.")

        if remaining_units <= 0:
            raise errors.ValidationError(f"You already have the maximum number of {entity_id} in play")

    # Finally, add the entity to the db
    entity_definition = datapacks.entities[entity_id]
    return velvet_dawn.db.units.spawn(
        entity_definition,
        player,
        x,
        y
    )


def remove_entity(player_id: str, x: int, y: int):
    """ Remove an entity from a cell

    Args:
        player_id: The player updating the map
        x: The column in the grid
        y: The row in the grid

    Raises:
        ValidationError: If user has no entity in the cell
    """
    if velvet_dawn.db.key_values.get_phase() != Phase.Setup:
        raise errors.ValidationError("Game setup may only be changed during game setup")

    units = [
        x for x in velvet_dawn.db.units.get_units_at_positions(Coordinate(x, y))
        if x.player == player_id
    ]
    if not units:
        raise errors.ValidationError("No entity for you to remove here.")

    for unit in units:
        velvet_dawn.db.units.remove(unit)


def validate_player_setups():
    """ This function checks all players have placed their commands """
    for player in velvet_dawn.players.list(exclude_spectators=True):
        player_entities: List[UnitInstance] = velvet_dawn.db.units.get_all_player_units(player.name)

        player_has_commander = False
        for item in player_entities:
            if datapacks.entities[item.entity_id].commander:
                player_has_commander = True

        if not player_has_commander:
            return False

    return True
