from abc import ABC
from typing import Union

from velvet_dawn.config import Config
from velvet_dawn.dao.models import UnitInstance, TileInstance


""" Abstract base action class

All other actions should derive from this class 
"""


class Action(ABC):

    def __init__(self):
        self.conditions = []

    @staticmethod
    def from_dict(id: str, data: dict):
        """ Parse the dict defined in the data-packs """
        pass

    def run(self, instance: Union[TileInstance, UnitInstance]):
        """ Execute the action """
        raise NotImplementedError
