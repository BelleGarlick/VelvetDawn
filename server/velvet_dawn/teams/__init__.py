from typing import List
from dao.initialisation import db
from dao.models.teams import Team


def list() -> List[Team]:
    return db.session.query(Team).all()


def auto_update_teams():
    # if game mode started, add empty players to spectatotors team
    # if game not started, get mode, if mode is singles then create new team, otherwise add to team with least players
    pass
