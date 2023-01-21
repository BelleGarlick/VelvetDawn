from typing import List
import velvet_dawn
from . import movement, upgrades, abilities

from ..db.instances import UnitInstance


def list(player: str = None, commander_only=False) -> List[UnitInstance]:
    if player:
        units = velvet_dawn.db.units.get_all_player_units(player)
    else:
        units = velvet_dawn.db.units.get_all_units()

    if commander_only:
        return [
            unit for unit in units
            if velvet_dawn.datapacks.entities[unit.entity_id].commander
        ]

    return units
