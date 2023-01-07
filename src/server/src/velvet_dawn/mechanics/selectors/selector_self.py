from typing import Union, List

from velvet_dawn.dao.models import TileInstance
from velvet_dawn.dao.models import UnitInstance
from .selector import Selector
from ...dao.models.world_instance import WorldInstance

""" Selector 'self' modifies what ever is calling it

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
            selector_name="self"
        )

    def new(self):
        return SelectorSelf()

    def get_selection(self, instance: Union[TileInstance, UnitInstance, WorldInstance]) -> List[Union[UnitInstance, TileInstance, WorldInstance]]:
        return self.filters.filter(instance, [instance])
