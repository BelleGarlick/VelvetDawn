import dataclasses
import enum
from abc import ABC
from typing import List, Union

from velvet_dawn import errors
from velvet_dawn.config import Config
from velvet_dawn.dao import db
from velvet_dawn.dao.models import UnitInstance, TileInstance


# todo not requals function


class SelectorParentType(enum.Enum):
    ANY = 0
    UNIT = 1
    TILE = 2


@dataclasses.dataclass
class Filter:
    key: str
    value: str

    @property
    def value_float(self): return float(self.value)


class Selector(ABC):
    def __init__(
            self,
            selector_name: str,
            parent_type: SelectorParentType,
            valid_filters: List[str] = None
    ):
        if not valid_filters: valid_filters = []

        self.full_selector = None
        self.attribute = None
        self.selector_name = selector_name
        self.parent_type = parent_type
        self.filters: List[Filter] = []
        self.__valid_filters = valid_filters

    def new(self) -> 'Selector':
        raise NotImplementedError()

    def instantiate(self, full_selector, filters: List[str], attribute: str) -> 'Selector':
        new_copy = self.new()
        new_copy.full_selector = full_selector
        new_copy.attribute = attribute

        if filters:
            for filter in filters:
                key, value = filter.split("=")
                if key not in self.__valid_filters:
                    raise errors.InvalidSelectorFilter(full_selector, key)
                new_copy.filters.append(Filter(key, value))

        return new_copy

    def get_selection(self, instance: Union[TileInstance, UnitInstance], config: Config) -> List[Union[UnitInstance, TileInstance]]:
        raise NotImplementedError()

    def function_set(self, instance: Union[TileInstance, UnitInstance], value: Union[str, int, float], config: Config):
        # TODO Check if valid and has attribute
        for item in self.get_selection(instance, config):
            item.set_attribute(self.attribute, value, commit=False)
        db.session.commit()

    def function_add(self, instance: Union[TileInstance, UnitInstance], value: Union[str, int, float], config: Config):
        for item in self.get_selection(instance, config):
            item.set_attribute(self.attribute, item.get_attribute(self.attribute, default=0) + value, commit=False)
        db.session.commit()

    def function_subtract(self, instance: Union[TileInstance, UnitInstance], value: Union[str, int, float], config: Config):
        for item in self.get_selection(instance, config):
            item.set_attribute(self.attribute, item.get_attribute(self.attribute, default=0) - value, commit=False)
        db.session.commit()

    def function_reset(self, instance: Union[TileInstance, UnitInstance], value: Union[str, int, float], config: Config):
        for item in self.get_selection(instance, config):
            item.reset_attribute(self.attribute, value, commit=False)
        db.session.commit()

    def function_multiply(self, instance: Union[TileInstance, UnitInstance], value: Union[str, int, float], config: Config):
        for item in self.get_selection(instance, config):
            item.set_attribute(self.attribute, item.get_attribute(self.attribute, default=0) * value, commit=False)
        db.session.commit()

    def function_add_tag(self, instance: Union[TileInstance, UnitInstance], value: Union[str, int, float], config: Config):
        for item in self.get_selection(instance, config):
            item.add_tag(value, commit=False)
        db.session.commit()

    def function_remove_tag(self, instance: Union[TileInstance, UnitInstance], value: Union[str, int, float], config: Config):
        for item in self.get_selection(instance, config):
            item.remove_tag(value, commit=False)
        db.session.commit()

    def function_equals(self, instance: Union[TileInstance, UnitInstance], value, config: Config):
        equal = True

        instances = self.get_selection(instance, config)
        if not instances:
            return False

        for item in self.get_selection(instance, config):
            if self.attribute:
                equal = equal and item.get_attribute(self.attribute, default=None) == value
            else:
                parent_id = item.tile_id if isinstance(item, TileInstance) else item.entity_id
                equal = equal and parent_id == value

        return equal
