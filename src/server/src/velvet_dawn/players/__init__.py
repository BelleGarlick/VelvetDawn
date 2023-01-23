import re
from typing import List, Optional

import velvet_dawn
from velvet_dawn import errors, constants
from velvet_dawn.dao import db
from velvet_dawn.dao.models import Player

from velvet_dawn.db.instances import UnitInstance, Instance


# noinspection PyShadowingBuiltins
def list(team: str = None, exclude_spectators: bool = False) -> List[Player]:
    if team:
        return db.session.query(Player).where(Player.team == team).all()

    if exclude_spectators:
        return db.session.query(Player)\
            .where(Player.team != constants.SPECTATORS_TEAM_ID)\
            .all()

    return db.session.query(Player).all()


def get_player(player_name: str) -> Optional[Player]:
    return db.session.query(Player).where(Player.name == player_name).one_or_none()


def join(player_name: str, password: str):
    """ Join the server

    First check the name is not matches regex, then load the player
    if the player doesn't exist then create the player and balance
    the teams.

    If the player does exist then check the password matches

    Args:
        player_name: The username the user joins the server with
        password: The password the user logins in with, to
            prevent other user's loging in.
    """
    if not re.fullmatch(r'[a-zA-Z0-9]{3,8}', player_name):
        raise errors.ValidationError("Names must be 3-8 characters long and letters & numbers only")

    player = get_player(player_name)
    if not player:
        player = Player(
            name=player_name,
            password=password,
            admin=not len(db.session.query(Player).all())
        )
        db.session.merge(player)
        db.session.commit()

    elif player.password != password:
        raise errors.ValidationError("Incorrect password.")

    # Update teams to balance players
    from .. import teams
    teams.auto_update_teams()

    return player


def get_friendly_enemy_players_breakdown(for_team: str):
    """ Get the sets of friendly and enemy players from
    the perspective of the given team. Spectators are
    not included

    Args:
        for_team: The team to get the split for

    Returns:
        tuple of the set if friendly and enemy teams
    """
    friendly_players = set()
    enemy_players = set()
    for player in list(exclude_spectators=True):
        if player.team == for_team:
            friendly_players.add(player.name)
        else:
            enemy_players.add(player.name)

    return friendly_players, enemy_players


def split_players_by_instance(instance: Instance):
    """ Get the sets of friendly and enemy players from the
    perspective of the given instance
    """
    if isinstance(instance, UnitInstance):
        player = velvet_dawn.players.get_player(instance.player)
        friendly_players, enemy_players = velvet_dawn.players.get_friendly_enemy_players_breakdown(player.team)

    else:
        team = velvet_dawn.game.turns.get_active_turn(velvet_dawn.game.phase.get_phase())
        friendly_players = {player.name for player in velvet_dawn.players.list() if player.team == team}
        enemy_players = {player.name for player in velvet_dawn.players.list() if player.team != team}

    return friendly_players, enemy_players
