from abc import ABC
from typing import List, Union, Optional

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
                if "=" in filter:
                    key, value = filter.split("=")
                    new_copy.filters.add_filter(key, value)
                else:
                    new_copy.filters.add_filter(filter)

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
            item.set_attribute(self.attribute, value)

    def function_add(self, instance: Union[TileInstance, UnitInstance], value: Union[str, int, float]):
        for item in self.get_chained_selection(instance):
            print(item.get_attribute(self.attribute, default=0))
            print(value)
            item.set_attribute(self.attribute, item.get_attribute(self.attribute, default=0) + value)

    def function_subtract(self, instance: Union[TileInstance, UnitInstance], value: Union[str, int, float]):
        for item in self.get_chained_selection(instance):
            item.set_attribute(self.attribute, item.get_attribute(self.attribute, default=0) - value)

    def function_reset(self, instance: Union[TileInstance, UnitInstance], value: Union[str, int, float]):
        for item in self.get_chained_selection(instance):
            item.reset_attribute(self.attribute, value)

    def function_multiply(self, instance: Union[TileInstance, UnitInstance], value: Union[str, int, float]):
        for item in self.get_chained_selection(instance):
            item.set_attribute(self.attribute, item.get_attribute(self.attribute, default=0) * value)

    def function_add_tag(self, instance: Union[TileInstance, UnitInstance], value: Union[str, int, float]):
        for item in self.get_chained_selection(instance):
            item.add_tag(value)

    def function_remove_tag(self, instance: Union[TileInstance, UnitInstance], value: Union[str, int, float]):
        for item in self.get_chained_selection(instance):
            item.remove_tag(value)

    def function_equals(self, instance: Union[TileInstance, UnitInstance], value):
        """ Compare if the given value is equal the selectors' id / attribute value """
        instances = self.get_chained_selection(instance)
        if not instances:
            return False

        for item in instances:
            if self.attribute: 
                if item.get_attribute(self.attribute, default=None) != value:
                    return False
            elif item.entity_id != value:
                return False

        return True

    def function_less_than(self, instance: Union[TileInstance, UnitInstance], value):
        """ Compare if the entities attribute is less than a given value """
        instances = self.get_chained_selection(instance)
        if not instances or not self.attribute:
            return False

        for item in instances:
            if item.get_attribute(self.attribute, default=None) >= int(value):
                return False

        return True

    def function_less_than_equals(self, instance: Union[TileInstance, UnitInstance], value):
        """ Compare if the entities attribute is less/equal than a given value """
        instances = self.get_chained_selection(instance)
        if not instances or not self.attribute:
            return False

        for item in instances:
            if item.get_attribute(self.attribute, default=0) > int(value):
                return False

        return True

    def function_get_value(self, instance: Union[TileInstance, UnitInstance]):
        """ This function effectively works to get the mean value of the data """
        instances = self.get_chained_selection(instance)
        n_instances = len(instances)
        if n_instances == 0:
            return 0

        all_string, string_value = True, None
        all_number, number_values = True, []

        for instance in instances:
            value = instance.get_attribute(self.attribute) if self.attribute else instance.id
            if value is not None:
                if isinstance(value, str):
                    all_number = False

                    if string_value is None:
                        string_value = value
                    elif string_value != value:
                        return None

                elif isinstance(value, int) or isinstance(value, float) or isinstance(value, bool):
                    all_string = False
                    number_values.append(float(value))
                else:
                    # Invalid type
                    return None

        if all_string and all_number:
            # Must have no valid values, e.g. all [None, None]
            return None

        if all_string:
            return string_value

        if all_number:
            if number_values:
                return sum(number_values) / len(number_values)
        return None

    def function_has_tag(self, instance: Union[TileInstance, UnitInstance], value: str):
        """ Check if the selection has a given tag """
        instances = self.get_chained_selection(instance)
        if not instances:
            return False

        for item in instances:
            if not item.has_tag(value):
                return False

        return True
