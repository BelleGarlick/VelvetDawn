from typing import Union

from velvet_dawn.dao.models import TileInstance, UnitInstance
from velvet_dawn.dao.models.world_instance import WorldInstance
from velvet_dawn.mechanics.conditionals.conditional import Conditional, Comparison


class ConditionalStandard(Conditional):
    """ This type of conditional compares if the selector matches the given value """

    def __init__(self):
        super().__init__(keyword="if")

    def is_true(self, instance: Union[UnitInstance, TileInstance, WorldInstance]) -> bool:
        """ Compare the values in the selector """
        if self.function == Comparison.EQUALS:
            return self.selector.function_equals(instance, self.function_value)

        if self.function == Comparison.NOT_EQUALS:
            return not self.selector.function_equals(instance, self.function_value)

        if self.function == Comparison.LESS_THAN:
            return self.selector.function_less_than(instance, self.function_value)

        if self.function == Comparison.LESS_THAN_EQUAL:
            return self.selector.function_less_than_equals(instance, self.function_value)

        if self.function == Comparison.GREATER_THAN:
            return not self.selector.function_less_than_equals(instance, self.function_value)

        if self.function == Comparison.GREATER_THAN_EQUAL:
            return not self.selector.function_less_than(instance, self.function_value)

        if self.function == Comparison.HAS_TAG:
            return self.selector.function_has_tag(instance, self.function_value)

        return False
