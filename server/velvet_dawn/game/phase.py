import velvet_dawn
from config import Config
from velvet_dawn.dao import db
from velvet_dawn.models.phase import Phase
from velvet_dawn.dao.models import Keys, Player


def get_phase():
    return velvet_dawn.dao.get_value(Keys.PHASE, default=Phase.Lobby)


def _set_phase(phase: Phase):
    velvet_dawn.dao.set_value(Keys.PHASE, phase)


def start_setup_phase(config: Config):
    print("Starting setup phase.")
    velvet_dawn.map.allocate_spawn_points(config)
    velvet_dawn.game.turns._update_turn_start_time()
    _set_phase(Phase.Setup)

    db.session.query(Player).update({Player.ready: False})
    db.session.commit()

    # TODO Check game setup is valid before people start placing


def start_game_phase():
    print("Starting game")
    _set_phase(Phase.GAME)

    db.session.query(Player).update({Player.ready: False})
    db.session.commit()

    # TODO if players haven't got a commander, move them to spectators

    # TODO Trigger entities on game start
    # TODO If game mode is CTF then trigger stuff here
