import dataclasses
from typing import Set, List

from velvet_dawn.dao.models.entity_setup import EntitySetup


@dataclasses.dataclass
class GameSetup:

    commanders: Set[str]
    units: List[EntitySetup]

    def json(self):
        return {
            "commanders": list(self.commanders),
            "units": {x.entity_id: x.amount for x in self.units}
        }
