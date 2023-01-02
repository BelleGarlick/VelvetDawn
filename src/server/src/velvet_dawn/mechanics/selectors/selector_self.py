from typing import Union, List

from velvet_dawn.dao.models import Tile
from velvet_dawn.dao.models import UnitInstance
from .selector import SelectorParentType, Selector
from ...config import Config

""" Selector 'self' for unit and tiles

Some examples:
 - {"targets": "self", "set": "civil-war:okay"}
 - {"if": "self", "equals": "civil-war:me"}
 - {"targets": "self.movement.weight", "set": 5}
 - {"if": "self.custom", "equals": 8}
 - {"if": "self", "equals": "civil-war:me"}
 - {"targets": "self.movement.weight", "set": 5}
 - {"targets": "self.health.max-health", "set": 5}
 - {"if": "self.attributes.custom", "equals": 8}
 - {"if": "self.combat.range", "equals": 8}
"""


class SelectorSelf(Selector):
    def __init__(self):
        Selector.__init__(
            self,
            selector_name="self",
            parent_type=SelectorParentType.ANY
        )

    def new(self):
        return SelectorSelf()

    def get_selection(self, instance: Union[Tile, UnitInstance], config: Config) -> List[Union[UnitInstance, Tile]]:
        return [instance]
