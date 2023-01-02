from typing import List

import velvet_dawn
from velvet_dawn.dao import db
from velvet_dawn.dao.models import UnitInstance, EntitySetup
from velvet_dawn import datapacks, errors
from velvet_dawn.models.game_setup import GameSetup
from velvet_dawn.models.phase import Phase

""" velvet_dawn.game.setup

This module handles the entity setup for the games. There
are functions for the admin to control the number of units
each player gets and if it's valid to start the game.

This module also contains functions for the player to place 
their initial setup entities when in the setup phase.
"""


def get_setup(player: str):
    # TODO Test this
    """ Get the game setup definition """
    entity_setup: List[EntitySetup] = db.session.query(EntitySetup).all()
    entity_setup = sorted(entity_setup, key=lambda x: x.entity_id)

    commander_entities = {
        entity.entity_id
        for entity in entity_setup
        if datapacks.entities[entity.entity_id].commander
    }

    units = {
        entity.entity_id: entity.amount for entity in entity_setup
        if not datapacks.entities[entity.entity_id].commander
    }

    # calculate remaining players
    placed_commander, remaining_units = False, {x: units[x] for x in units}
    player_entities = db.session.query(UnitInstance).where(UnitInstance.player == player).all()
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
    if velvet_dawn.game.phase.get_phase() != Phase.Lobby:
        raise errors.ValidationError("Game setup units may only be changed in the lobby by the admin")

    # Check entity exists
    if entity_id not in datapacks.entities:
        raise errors.ValidationError(f"Unknown entity id: '{entity_id}'")

    # If exists, update else create
    item = db.session.query(EntitySetup).where(EntitySetup.entity_id == entity_id).one_or_none()
    if item:
        query = db.session.query(EntitySetup).where(EntitySetup.entity_id == entity_id)
        if count > 0:
            query.update({EntitySetup.amount: count})
        else:
            for item in query.all():
                db.session.delete(item)

    elif count > 0:
        db.session.add(EntitySetup(entity_id=entity_id, amount=count))

    db.session.commit()


def is_setup_valid(player):
    """ Setup definitions must contain commanders """
    return bool(get_setup(player).commanders)


def place_entity(player: str, entity_id: str, x: int, y: int):
    if velvet_dawn.game.phase.get_phase() != Phase.Setup:
        raise errors.ValidationError("Game setup may only be changed during game setup")

    setup = get_setup(player)

    if entity_id not in datapacks.entities:
        raise errors.UnknownEntityError(entity_id)

    if not velvet_dawn.map.is_point_spawnable(user=player, x=x, y=y):
        raise errors.ValidationError("This point is not within your spawn territory")

    if not velvet_dawn.map.is_traversable(x=x, y=y):
        raise errors.ValidationError("Cannot place two entities in the same tile.")

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
    entity = UnitInstance(
        player=player,
        entity_id=entity_id,
        x=x,
        y=y
    )
    db.session.add(entity)
    db.session.commit()
    entity_definition.attributes.save_to_db(entity, entity_definition)


def remove_entity(player_id: str, x: int, y: int):
    """ Remove an entity from a cell

    Args:
        player_id: The player updating the map
        x: The column in the grid
        y: The row in the grid

    Raises:
        ValidationError: If user has no entity in the cell
    """
    if velvet_dawn.game.phase.get_phase() != Phase.Setup:
        raise errors.ValidationError("Game setup may only be changed during game setup")

    entities = db.session.query(UnitInstance).where(
        UnitInstance.player == player_id,
        UnitInstance.x == x,
        UnitInstance.y == y
    ).all()

    if not entities:
        raise errors.ValidationError("No entity for you to remove here.")

    for entity in entities:
        db.session.delete(entity)
    db.session.commit()


def validate_player_setups():
    """ This function checks all players have placed their commands """
    for player in velvet_dawn.players.list(exclude_spectators=True):
        player_entities: List[UnitInstance] = db.session.query(UnitInstance).where(UnitInstance.player == player.name).all()

        player_has_commander = False
        for item in player_entities:
            if datapacks.entities[item.entity_id].commander:
                player_has_commander = True

        if not player_has_commander:
            return False

    return True
