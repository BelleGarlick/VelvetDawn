import re
from typing import List, Optional
from dao.initialisation import db
from dao.models import Player


# noinspection PyShadowingBuiltins


def list() -> List[Player]:
    return db.session.query(Player).all()


def get_player(player_name: str) -> Optional[Player]:
    return db.session.query(Player).where(Player.name == player_name).one_or_none()


def join(player_name: str):
    if not player_name:
        raise Exception(f"Name '{player_name}' not valid.")

    if not re.fullmatch(r'[a-zA-Z]{3,8}', player_name):
        raise Exception("Names must be 3-8 characters long and letters only")

    # TODO Also validate the url where th eplayer is coming from to check is valid
    if not get_player(player_name):
        db.session.merge(Player(
            name=player_name
        ))

    # Update teams to balance players
    from .. import teams
    teams.auto_update_teams()
