import enum

from dao.initialisation import db
from dao.models import Keys, KeyValues


class Phase(int, enum.Enum):
    Lobby = 0
    SETUP = 1
    GAME = 2


def phase():
    phase = db.session.query(KeyValues).where(KeyValues.key == Keys.PHASE).one_or_none()
    if phase:
        return int(phase.value)

    return Phase.Lobby


def turn():
    turn = db.session.query(KeyValues).where(KeyValues.key == Keys.TURN).one_or_none()
    if turn:
        return int(turn.value)

    return -1


def active_turn():
    turn = db.session.query(KeyValues).where(KeyValues.key == Keys.ACTIVE_TURN).one_or_none()
    if turn:
        return turn.value

    # Stores a players name of team::team_name

    return None
