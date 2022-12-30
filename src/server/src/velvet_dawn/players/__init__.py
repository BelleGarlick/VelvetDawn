import re
from typing import List, Optional

from velvet_dawn import errors, constants
from velvet_dawn.dao import db
from velvet_dawn.dao.models import Player


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

        # Update teams to balance players
        from .. import teams
        teams.auto_update_teams()

    elif player.password != password:
        raise errors.ValidationError("Incorrect password.")

    return player
