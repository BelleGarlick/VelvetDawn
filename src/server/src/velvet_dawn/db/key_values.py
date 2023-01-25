from typing import Union

import velvet_dawn.db.gateway as db
from velvet_dawn.db.models import Phase

""" Key's interface

Used to store specific small peices of information such as the 
game state / phase.
"""


KEYS_KEY = "KEYS#{}"


def _set(key: str, value: Union[int, float, str, bool]):
    db.set_value(KEYS_KEY.format(key), value)
    return value


def _get(key, default: Union[int, float, str, bool] = None) -> Union[int, float, str, bool]:
    return db.get_value(KEYS_KEY.format(key), default=default)


def get_phase() -> Phase:
    # noinspection PyTypeChecker
    return _get('phase', Phase.Lobby)


def set_phase(phase: Phase):
    _set("phase", phase)


def get_map_size():
    value = _get("map-size")
    if value:
        x, y = value.split(":")
        return int(x), int(y)

    return None, None


def set_map_size(width: int, height: int):
    _set("map-size", f"{width}:{height}")


def set_turn_start(start_time: float):
    return _set("turn-start", start_time)


def get_turn_start(default=None):
    return _get("turn-start", default)


def get_active_turn():
    return _get("active-turn")


def set_active_turn(new_team_turn: str) -> str:
    return _set("active-turn", new_team_turn)


def set_turn_number(turn_number):
    return _set("turn-number", turn_number)
