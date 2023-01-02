import velvet_dawn.units
from velvet_dawn.dao.models import Tile
from .selector import SelectorParentType, Selector
from ...config import Config

""" Selector 'unit' references the unit in the current tile

Some examples:
 - {"targets": "unit.movement.weight", "add": 5}
"""
# TODO Validate the selector has the attributes before calling add, set, subtract, multiple


class SelectorUnit(Selector):
    def __init__(self):
        Selector.__init__(self, selector_name="unit", parent_type=SelectorParentType.TILE)

    def new(self):
        return SelectorUnit()

    def get_selection(self, instance: Tile, config: Config):
        unit = velvet_dawn.units.get_unit_at_position(x=instance.x, y=instance.y)
        if unit:
            return [unit]
        return []
