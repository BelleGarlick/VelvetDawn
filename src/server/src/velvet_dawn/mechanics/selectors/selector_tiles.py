from typing import Union, List

import velvet_dawn
from .selector import Selector
from ...db.instances import Instance, TileInstance, UnitInstance, WorldInstance

""" Selector 'tile' references the tile the current unit is in

Some examples:
 - {"targets": "tile.movement.weight", "add": 5}
"""


class SelectorTile(Selector):
    """ Get the tile of the position of the given instance """

    def __init__(self):
        Selector.__init__(self, selector_name="tile")

    def new(self):
        return SelectorTile()

    def get_selection(self, instance: Instance) -> List[Instance]:
        if isinstance(instance, TileInstance):
            return self.filters.filter(instance, [instance])

        if isinstance(instance, UnitInstance):
            tile = velvet_dawn.db.tiles.get_tile(x=instance.x, y=instance.y)
            if tile:
                return self.filters.filter(instance, [tile])

        return []


class SelectorTiles(Selector):
    """ Get a list of tiles """

    def __init__(self):
        Selector.__init__(self, selector_name="tiles")

    def new(self):
        return SelectorTiles()

    def get_selection(self, instance: Union[TileInstance, UnitInstance, WorldInstance]) -> List[Instance]:
        return self.filters.filter(instance, velvet_dawn.db.tiles.all())
