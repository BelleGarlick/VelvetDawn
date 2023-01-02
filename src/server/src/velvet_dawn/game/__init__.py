import time

import velvet_dawn.teams
from velvet_dawn import constants
from velvet_dawn.config import Config
from velvet_dawn.dao import db
from velvet_dawn.dao.models import UnitInstance
from velvet_dawn.dao.models.attributes import TileAttribute, UnitAttribute

from velvet_dawn.models.game_state import GameState
from velvet_dawn.models.mode import Mode
from velvet_dawn.models.phase import Phase
from velvet_dawn.game import phase, turns, setup


# TODO Test this with auto team balanacing
def mode():
    # if in game raise exception, can't change
    # Change game mode, delete all teams, then auto balance
    # otherwise just return
    return Mode.ALL_V_ALL


def get_state(config: Config, user: str, full_state: bool = False):
    current_phase = phase.get_phase()

    spawn_area = []
    if current_phase == Phase.Setup:
        spawn_area = velvet_dawn.map.spawn.get_allocated_spawn_area(user)

    entities = db.session.query(UnitInstance).all()

    # Get the latest attribute changes
    valid_update_time_bound = time.time() - constants.PARTIAL_GAME_STATE_TIME
    unit_attr_changes = [
        attr for attr in db.session.query(UnitAttribute).all()
        if full_state or attr.update_time > valid_update_time_bound
    ]
    tile_attribute_changes = [
        attr for attr in db.session.query(TileAttribute).all()
        if full_state or attr.update_time > valid_update_time_bound
    ]

    return GameState(
        phase=current_phase,
        turn=turns.current_turn_data(config, current_phase),
        teams=velvet_dawn.teams.list(),
        players=velvet_dawn.players.list(),
        setup=velvet_dawn.game.setup.get_setup(user),
        spawn_area=spawn_area,
        entities=entities,
        unit_attr_changes=unit_attr_changes,
        tile_attr_changes=tile_attribute_changes
    )
