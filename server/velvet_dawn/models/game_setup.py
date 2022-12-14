import dataclasses
from typing import Set, List

from dao.models.entity_setup import EntitySetup


@dataclasses.dataclass
class GameSetup:
    commanders: Set[str]
    units: List[EntitySetup]

    def json(self):
        return {
            "commanders": self.commanders,
            "units": [x.json() for x in self.units]
        }
