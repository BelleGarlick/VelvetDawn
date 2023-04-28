from abc import ABC
from typing import Union, Dict

from velvet_dawn.models.coordinate import Coordinate


class Instance(ABC):
    def __init__(self, datapack_id: str, instance_id: str):
        self._datapack_id = datapack_id
        self._instance_id = instance_id

        self.tags = set()
        self.attributes: Dict[str, Union[float, str, bool]] = {}
        self.position = Coordinate(0, 0)

    @property
    def datapack_id(self):
        return self._datapack_id

    @property
    def instance_id(self):
        return self._instance_id

    def __hash__(self):
        raise NotImplementedError

    def __eq__(self, other):
        return hash(self) == hash(other)

    def set_attribute(self, key, value):
        raise NotImplementedError

    def get_attribute(self, key, default=None):
        raise NotImplementedError

    def reset_attribute(self, key, value_if_not_exists):
        raise NotImplementedError

    def add_tag(self, tag: str):
        # TODO Remove
        self.tags.add(tag)

    def remove_tag(self, tag: str):
        # TODO Remove
        self.tags.remove(tag)

    def has_tag(self, tag: str):
        raise NotImplementedError


class WorldInstance(Instance):

    instance = None

    def __init__(self):
        super().__init__("world", "world")

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(WorldInstance, cls).__new__(cls)
        return cls.instance
