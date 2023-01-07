from abc import ABC
from typing import Union, List

from velvet_dawn import errors
from velvet_dawn.dao.models import UnitInstance, TileInstance
from velvet_dawn.dao.models.world_instance import WorldInstance
from velvet_dawn.mechanics.conditionals.conditional import Conditional

""" Abstract base action class

All other actions should derive from this class 
"""


class Action(ABC):

    def __init__(self):
        self.conditions: List[Conditional] = []

    @staticmethod
    def from_dict(id: str, data: dict):
        """ Parse the dict defined in the data-packs """
        pass

    def run(self, instance: Union[TileInstance, UnitInstance, WorldInstance]):
        """ Execute the action """
        raise NotImplementedError

    def can_run(self, instance: Union[TileInstance, UnitInstance, WorldInstance]):
        """ Test if the action can run """
        for condition in self.conditions:
            if not condition.is_true(instance):
                return False
        return True
