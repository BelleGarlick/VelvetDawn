from dao.initialisation import db
from dao.models import Keys, KeyValues
from velvet_dawn.models.mode import Mode
from velvet_dawn.models.phase import Phase


# TODO Test this with auto team balanacing
def mode():
    # if in game raise exception, can't change
    # Change game mode, delete all teams, then auto balance
    # otherwise just return
    return Mode.ALL_V_ALL


def initial_entities():
    return {
        "civil-war:commander": 1,
        "civil-war:general": 3,
        "civil-war:pikemen": 6,
        "civil-war:cavalry": 3,
        "civil-war:cannons": 2,
        "civil-war:medics": 1,
        "civil-war:musketeers": 6
    }


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
