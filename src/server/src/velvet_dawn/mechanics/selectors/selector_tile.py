import velvet_dawn
from velvet_dawn.dao.models import UnitInstance
from .selector import SelectorParentType, Selector
from ...config import Config

""" Selector 'tile' references the tile the current unit is in

Some examples:
 - {"targets": "tile.movement.weight", "add": 5}
"""


class SelectorTile(Selector):
    def __init__(self):
        Selector.__init__(self, selector_name="tile", parent_type=SelectorParentType.UNIT)

    def new(self):
        return SelectorTile()

    def get_selection(self, instance: UnitInstance, config: Config):
        tile = velvet_dawn.map.get_tile(x=instance.x, y=instance.y)
        if tile:
            return [tile]
        return []
