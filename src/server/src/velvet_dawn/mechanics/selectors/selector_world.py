from typing import Union, List

from velvet_dawn.dao.models import TileInstance
from velvet_dawn.dao.models import UnitInstance
from .selector import Selector
from ...dao.models.world_instance import WorldInstance


""" Selector 'world' allows the user to access the world object 
in order to set/get attributes

Some examples:
 - {"targets": "world.turns", "set": "5"}
 - {"targets": "world.players-count", "subtract": "2"}
"""


class SelectorWorld(Selector):
    def __init__(self):
        Selector.__init__(self, selector_name="world")

    def new(self):
        return SelectorWorld()

    def get_selection(self, instance: Union[TileInstance, UnitInstance, WorldInstance]) -> List[WorldInstance]:
        # World is singleton so this will return the same instance
        return self.filters.filter(instance, [WorldInstance()])
