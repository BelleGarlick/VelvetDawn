from typing import List

import velvet_dawn
from .selector import Selector
from ...db.instances import UnitInstance, Instance

""" Selector 'commander' references to the commander of the given unit

Some examples:
 - {"targets": "unit[]>commander[].movement.weight", "add": 5}
"""


class SelectorCommander(Selector):
    """ Get the commander of the unit given """

    def __init__(self):
        Selector.__init__(self, selector_name="commander")

    def new(self):
        return SelectorCommander()

    def get_selection(self, instance: Instance):
        if isinstance(instance, UnitInstance):
            commanders = velvet_dawn.units.list(commander_only=True)
            commanders = list(filter(lambda x: x.player == instance.player, commanders))
            return self.filters.filter(instance, commanders)
        return []


class SelectorCommanders(Selector):
    """ Get all commanders in the game """

    def __init__(self):
        Selector.__init__(self, selector_name="commanders")

    def new(self):
        return SelectorCommanders()

    def get_selection(self, instance: Instance):
        return self.filters.filter(instance, velvet_dawn.units.list(commander_only=True))


class SelectorFriendlyCommanders(Selector):
    """ Get friendly commanders in the game """

    def __init__(self):
        Selector.__init__(self, selector_name="commanders-friendly")

    def new(self):
        return SelectorFriendlyCommanders()

    def get_selection(self, instance: Instance) -> List[Instance]:
        units = velvet_dawn.units.list(commander_only=True)
        friendly_players, _ = velvet_dawn.players.split_players_by_instance(instance)
        friendly_units = list(filter(lambda x: x.player in friendly_players, units))

        return self.filters.filter(instance, friendly_units)


class SelectorEnemyCommanders(Selector):
    """ Get the list of enemy commanders """

    def __init__(self):
        Selector.__init__(self, selector_name="commanders-enemy")

    def new(self):
        return SelectorEnemyCommanders()

    def get_selection(self, instance: Instance) -> List[Instance]:
        units = velvet_dawn.units.list(commander_only=True)
        _, enemy_players = velvet_dawn.players.split_players_by_instance(instance)
        enemy_units = list(filter(lambda x: x.player in enemy_players, units))

        return self.filters.filter(instance, enemy_units)
