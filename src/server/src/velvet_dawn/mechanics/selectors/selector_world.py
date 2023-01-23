from typing import List

from .selector import Selector
from ...db.instances import Instance, WorldInstance

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

    def get_selection(self, instance: Instance) -> List[Instance]:
        # World is singleton so this will return the same instance
        return self.filters.filter(instance, [WorldInstance()])
