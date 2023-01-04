from abc import ABC
from typing import Union, Type

from velvet_dawn.config import Config
from velvet_dawn.dao.models import UnitInstance, TileInstance
from velvet_dawn.models import Unit, Tile


""" Abstract base action class

All other actions should derive from this class 
"""


class Action(ABC):

    def __init__(self):
        self.conditions = []

    @staticmethod
    def from_dict(id: str, parent_type: Union[Type[Unit], Type[Tile]], data: dict):
        """ Parse the dict defined in the datapacks """
        pass

    def run(self, instance: Union[TileInstance, UnitInstance], config: Config):
        """ Execute the action """
        raise NotImplementedError
