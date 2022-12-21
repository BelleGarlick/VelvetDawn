import velvet_dawn.teams
from velvet_dawn.dao import db
from velvet_dawn.dao.models import Keys, KeyValues
from velvet_dawn.models.game_state import GameState
from velvet_dawn.models.mode import Mode
from velvet_dawn.models.phase import Phase
from velvet_dawn.game import setup


# TODO Test this with auto team balanacing
def mode():
    # if in game raise exception, can't change
    # Change game mode, delete all teams, then auto balance
    # otherwise just return
    return Mode.ALL_V_ALL


def phase(set: Phase = None):
    phase = db.session.query(KeyValues).where(KeyValues.key == Keys.PHASE).one_or_none()

    if set:
        if phase:
            db.session.query(KeyValues).where(KeyValues.key == Keys.PHASE).update({
                KeyValues.value: set
            })
        else:
            db.session.add(KeyValues(key=Keys.PHASE, value=set))
        db.session.commit()
        return

    if phase:
        return phase.value

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


def start_setup_phase(config):
    velvet_dawn.map.allocate_spawn_points(config)
    phase(set=Phase.Setup)
    # TODO Check game setup is valid before people start placing


def get_state(user: str):
    return GameState(
        phase=phase(),
        turn=turn(),
        active_turn=active_turn(),
        teams=velvet_dawn.teams.list(),
        players=velvet_dawn.players.list(),
        setup=velvet_dawn.game.setup.get_setup(),
        spawn_area=velvet_dawn.map.spawn.get_allocated_spawn_area(user)
    )
