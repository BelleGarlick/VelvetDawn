from typing import List

import velvet_dawn
from .selector import Selector
from ...db.instances import UnitInstance, TileInstance, Instance
from ...models.coordinate import Coordinate

""" Units selectors, allow the user to get the units in the game """


class SelectorUnit(Selector):
    """ Get a single unit in the same position as the given instance """

    def __init__(self):
        Selector.__init__(self, selector_name="unit")

    def new(self):
        return SelectorUnit()

    def get_selection(self, instance: Instance):
        """ Get the unit in the same position as the given instance """
        if isinstance(instance, UnitInstance):
            return self.filters.filter(instance, [instance])

        if isinstance(instance, TileInstance):
            unit = velvet_dawn.db.units.get_units_at_positions(Coordinate(instance.x, instance.y))
            if unit:
                return self.filters.filter(instance, unit)

        return []


class SelectorUnits(Selector):
    """ Get all units in the game """

    def __init__(self):
        Selector.__init__(self, selector_name="units")

    def new(self):
        return SelectorUnits()

    def get_selection(self, instance: Instance) -> List[Instance]:
        """ Return all units """
        return self.filters.filter(instance, velvet_dawn.units.list())


class SelectorEnemies(Selector):
    """ Get the enemy units from the perspective of the
    unit's player or the games current turn """

    def __init__(self):
        Selector.__init__(self, selector_name="enemies")

    def new(self):
        return SelectorEnemies()

    def get_selection(self, instance: Instance) -> List[Instance]:
        """ Get the list of selectors who are not on the same team / who's turn it isn't """
        units = velvet_dawn.units.list()

        _, enemy_players = velvet_dawn.players.split_players_by_instance(instance)
        enemy_units = list(filter(lambda x: x.player in enemy_players, units))

        return self.filters.filter(instance, enemy_units)


class SelectorFriendlies(Selector):
    """ Get the friendly units from the perspective of the
    unit's player or the games current turn """

    def __init__(self):
        Selector.__init__(self, selector_name="friendlies")

    def new(self):
        return SelectorFriendlies()

    def get_selection(self, instance: Instance) -> List[Instance]:
        """ Get the list of selectors who are on the same team / who's turn it is """
        units = velvet_dawn.units.list()

        friendly_players, _ = velvet_dawn.players.split_players_by_instance(instance)
        friendly_units = list(filter(lambda x: x.player in friendly_players, units))

        return self.filters.filter(instance, friendly_units)
