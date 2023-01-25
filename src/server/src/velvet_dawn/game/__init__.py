import velvet_dawn.teams
from velvet_dawn.config import Config
from velvet_dawn.db.models import Phase

from velvet_dawn.models.game_state import GameState
from velvet_dawn.models.mode import Mode
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

    if full_state:
        attribute_updates = velvet_dawn.db.attributes.get_full_attribute_list()
        unit_changes = {
            "updates": [x.json() for x in velvet_dawn.db.units.get_all_units()],
            "removed": []
        }

    else:
        unit_changes = velvet_dawn.db.units.get_updates()
        attribute_updates = velvet_dawn.db.attributes.get_attribute_updates()

    return GameState(
        phase=current_phase,
        turn=turns.current_turn_data(config, current_phase),
        teams=velvet_dawn.teams.list(),
        players=velvet_dawn.players.list(),
        setup=velvet_dawn.game.setup.get_setup(user),
        spawn_area=spawn_area,
        unit_changes=unit_changes,
        attr_changes=attribute_updates,
    )
