from typing import Dict

import velvet_dawn.db.instance as db


""" This file writes the number of allowed units in the 
game's setup to the db.
"""


# Store the unit ids and count using this key.
SETUP_UNITS_KEY = "UNITS-SETUP"


def set_count(unit_id: str, count: int):
    db.hset(SETUP_UNITS_KEY, unit_id, count)


def get() -> Dict[str, int]:
    return db.hgetall(SETUP_UNITS_KEY)