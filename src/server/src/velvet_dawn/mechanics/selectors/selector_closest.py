from typing import Union, List

import velvet_dawn
from velvet_dawn.dao.models import TileInstance, UnitInstance
from .selector import Selector
from ...dao.models.world_instance import WorldInstance


""" Selector 'unit' references the unit in the current tile

Some examples:
 - {"targets": "unit.movement.weight", "add": 5}
"""


def get_closest(to: Union[TileInstance, UnitInstance], items: List[Union[TileInstance, UnitInstance]]):
    closest, best_distance = None, 0

    if isinstance(to, TileInstance) or isinstance(to, UnitInstance):
        for item in items:
            # Don't want to include itself otherwise this will always return self
            if item.id == to.id and isinstance(to, type(item)):
                continue

            distance = velvet_dawn.map.get_distance(to, item)

            if not closest:
                closest = item
                best_distance = distance
            elif distance < best_distance:
                closest = item
                best_distance = distance

    return [closest] if closest else []


class SelectorClosest(Selector):
    """ Get the closest unit to the given instance """

    def __init__(self):
        Selector.__init__(self, selector_name="closest")

    def new(self):
        return SelectorClosest()

    def get_selection(self, instance: Union[TileInstance, UnitInstance, WorldInstance]):
        units = self.filters.filter(instance, velvet_dawn.units.list())
        return get_closest(instance, units)


class SelectorClosestEnemy(Selector):
    """ Get the closest enemy to the given instance """

    def __init__(self):
        Selector.__init__(self, selector_name="closest-enemy")

    def new(self):
        return SelectorClosestEnemy()

    def get_selection(self, instance: Union[TileInstance, UnitInstance, WorldInstance]) -> List[UnitInstance]:
        units = velvet_dawn.units.list()
        _, enemy_players = velvet_dawn.players.split_players_by_instance(instance)
        enemy_units = list(filter(lambda x: x.player in enemy_players, units))
        enemy_units = self.filters.filter(instance, enemy_units)

        return get_closest(instance, enemy_units)


class SelectorClosestFriendly(Selector):
    """ Get the closest friendly to the given instance """

    def __init__(self):
        Selector.__init__(self, selector_name="closest-friendly")

    def new(self):
        return SelectorClosestFriendly()

    def get_selection(self, instance: Union[TileInstance, UnitInstance]) -> List[Union[UnitInstance, TileInstance]]:
        units = velvet_dawn.units.list()
        friendly_players, _ = velvet_dawn.players.split_players_by_instance(instance)
        friendly_units = list(filter(lambda x: x.player in friendly_players, units))
        friendly_units = self.filters.filter(instance, friendly_units)

        return get_closest(instance, friendly_units)
