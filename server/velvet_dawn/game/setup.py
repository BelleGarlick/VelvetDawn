from typing import List

import errors
import velvet_dawn
from velvet_dawn.dao import db
from velvet_dawn.dao.models import Entity as DbEntity, Player
from velvet_dawn.dao.models.entity_setup import EntitySetup
from velvet_dawn import datapacks
from velvet_dawn.models.game_setup import GameSetup
from velvet_dawn.models.phase import Phase

""" velvet_dawn.game.setup

This module handles the entity setup for the games. There
are functions for the admin to control the number of units
each player gets and if it's valid to start the game.

This module also contains fucntions for the player to place 
their initial setup entities when in the setup phase.
"""


def get_setup():
    """ Get the game setup definition """
    entity_setup: List[EntitySetup] = db.session.query(EntitySetup).all()
    entity_setup = sorted(entity_setup, key=lambda x: x.entity_id)

    return GameSetup(
        commanders={
            entity.entity_id
            for entity in entity_setup
            if datapacks.entities[entity.entity_id].commander
        },
        units=[
            entity for entity in entity_setup
            if not datapacks.entities[entity.entity_id].commander
        ]
    )


def update_setup(entity_id: str, count: int):
    """ Update the initial entities a player may use

    Args:
        entity_id: The id to update the count for
        count: Number of items the user can start with
            If the entity is a commaner then this will
            be ignored.
    """
    if velvet_dawn.game.phase() != Phase.Lobby:
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
            print("deleting")
            for item in query.all():
                db.session.delete(item)

    elif count > 0:
        print("adding")
        db.session.add(EntitySetup(entity_id=entity_id, amount=count))

    db.session.commit()


def is_setup_valid():
    """ Setups must contain commanders """
    return bool(get_setup().commanders)


def place_entity(player, entity_id, x, y):
    if velvet_dawn.game.phase() != Phase.Setup:
        raise errors.ValidationError("Game setup may only be changed during game setup")

    setup = get_setup()
    existing_entities = db.session.query(DbEntity).where(DbEntity.player == player, DbEntity.entity_id == entity_id).all()

    if entity_id not in datapacks.entities:
        raise errors.UnknownEntityError(entity_id)

    # TODO Check within the starting territory

    if not velvet_dawn.map.is_placeable(x=x, y=y):
        raise errors.ValidationError("Cannot place two entities in the same tile.")

    # Check that the entity is valid within the setup definition
    if entity_id in setup.commanders:
        # Check they don't already have a commander
        if existing_entities:
            raise errors.ValidationError("You already have a commander in play")
    else:
        entitie_setup_definition: List[EntitySetup] = list(filter(lambda unit: unit.entity_id, setup.units))
        if entitie_setup_definition:
            if len(existing_entities) >= entitie_setup_definition[0].amount:
                raise errors.ValidationError(f"You already have the maximum number of {entity_id} in play")

        else:
            raise errors.EntityMissingFromSetupDefinition(f"Enitity {entity_id} not included in the setup definition.")

    # Finally, add the entity to the db
    db.session.add(DbEntity(
        player=player,
        entity_id=entity_id,
        pos_x=x,
        pos_y=y
    ))
    db.session.commit()


def remove_entity(player_id: str, x: int, y: int):
    """ Remove an entity from a cell

    Args:
        player_id: The player updating the map
        x: The column in the grid
        y: The row in the grid

    Raises:
        ValidationError: If user has no entity in the cell
    """
    if velvet_dawn.game.phase() != Phase.Setup:
        raise errors.ValidationError("Game setup may only be changed during game setup")

    entity = db.session.query(DbEntity).where(
        DbEntity.player == player_id,
        DbEntity.pos_x == x,
        DbEntity.pos_y == y
    ).one_or_none()

    if not entity:
        raise errors.ValidationError("No entity for you to remove here.")

    db.session.delete(entity)
    db.session.commit()


def validate_player_setups():
    """ This function checks all players have placed their commands """
    players = db.session.query(Player).all()

    for player in players:
        player_entities: List[DbEntity] = db.session.query(DbEntity).where(DbEntity.player == player.name).all()

        player_has_commander = False
        for item in player_entities:
            if datapacks.entities[item.entity_id].commander:
                player_has_commander = True

        if not player_has_commander:
            return False

    return True
