import dataclasses
from typing import Set, Dict


@dataclasses.dataclass
class GameSetup:

    commanders: Set[str]
    units: Dict[str, int]
    placed_commander: bool
    remaining_units: Dict[str, int]

    def json(self):
        return {
            "commanders": list(self.commanders),
            "units": self.units,
            "placedCommander": self.placed_commander,
            "remainingUnits": self.remaining_units
        }
