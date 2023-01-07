from abc import ABC
from typing import List, Union, Optional

from velvet_dawn.dao import db
from velvet_dawn.dao.models import UnitInstance, TileInstance

from velvet_dawn.dao.models.world_instance import WorldInstance
from velvet_dawn.mechanics.selectors.filters import Filters


class Selector(ABC):
    def __init__(
            self,
            selector_name: str,
    ):
        self.full_selector = None
        self.attribute = None
        self.selector_name = selector_name
        self.filters: Filters = Filters()

        self.chained_selector: Optional[Selector] = None

    def new(self) -> 'Selector':
        raise NotImplementedError()

    def instantiate(self, full_selector, filters: List[str], attribute: str) -> 'Selector':
        new_copy = self.new()
        new_copy.full_selector = full_selector
        new_copy.attribute = attribute

        if filters:
            for filter in filters:
                key, value = filter.split("=")
                new_copy.filters.add_filter(key, value)

        return new_copy

    def get_selection(
            self,
            instance: Union[TileInstance, UnitInstance, WorldInstance]
    ) -> List[Union[UnitInstance, TileInstance, WorldInstance]]:
        raise NotImplementedError()

    def get_chained_selection(self, instance: Union[TileInstance, UnitInstance, WorldInstance]) -> List[Union[UnitInstance, TileInstance, WorldInstance]]:
        direct_selection = self.get_selection(instance)

        if not self.chained_selector:
            return direct_selection

        chained_selection = set()
        for item in direct_selection:
            chained_selection.update(self.chained_selector.get_chained_selection(item))

        return list(chained_selection)

    def function_set(self, instance: Union[TileInstance, UnitInstance], value: Union[str, int, float]):
        for item in self.get_chained_selection(instance):
            item.set_attribute(self.attribute, value, commit=False)
        db.session.commit()

    def function_add(self, instance: Union[TileInstance, UnitInstance], value: Union[str, int, float]):
        for item in self.get_chained_selection(instance):
            item.set_attribute(self.attribute, item.get_attribute(self.attribute, default=0) + value, commit=False)
        db.session.commit()

    def function_subtract(self, instance: Union[TileInstance, UnitInstance], value: Union[str, int, float]):
        for item in self.get_chained_selection(instance):
            item.set_attribute(self.attribute, item.get_attribute(self.attribute, default=0) - value, commit=False)
        db.session.commit()

    def function_reset(self, instance: Union[TileInstance, UnitInstance], value: Union[str, int, float]):
        for item in self.get_chained_selection(instance):
            item.reset_attribute(self.attribute, value, commit=False)
        db.session.commit()

    def function_multiply(self, instance: Union[TileInstance, UnitInstance], value: Union[str, int, float]):
        for item in self.get_chained_selection(instance):
            item.set_attribute(self.attribute, item.get_attribute(self.attribute, default=0) * value, commit=False)
        db.session.commit()

    def function_add_tag(self, instance: Union[TileInstance, UnitInstance], value: Union[str, int, float]):
        for item in self.get_chained_selection(instance):
            item.add_tag(value, commit=False)
        db.session.commit()

    def function_remove_tag(self, instance: Union[TileInstance, UnitInstance], value: Union[str, int, float]):
        for item in self.get_chained_selection(instance):
            item.remove_tag(value, commit=False)
        db.session.commit()

    def function_equals(self, instance: Union[TileInstance, UnitInstance], value):
        equal = True

        instances = self.get_chained_selection(instance)
        if not instances:
            return False

        for item in instances:
            if self.attribute:
                equal = equal and item.get_attribute(self.attribute, default=None) == value
            else:
                parent_id = item.tile_id if isinstance(item, TileInstance) else item.entity_id
                equal = equal and parent_id == value

        return equal
