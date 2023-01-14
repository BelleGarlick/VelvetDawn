import enum
import random
from typing import Optional

import velvet_dawn.mechanics.selectors
from velvet_dawn.mechanics.selectors import Selector


""" Function values are the values which conditionals are
compared to or modify actions are set to. This class
parses the values to check if it should be random, a
selector or a specific value.

Raw value:
 - {"if": '...', "gt": "example"}
 
Selector value:
 - {"if": '...', "gt": "@self.attribute"}
 
Random value:
 - {"if": '...', "gt": "__rand__"}
"""


class FunctionValueType(enum.Enum):
    RAW = 0
    SELECTOR = 1
    RANDOM = 2


class FunctionValue:
    def __init__(self):
        self.value_type = FunctionValueType.RAW
        self._selector_value: Optional[Selector] = None
        self._raw_value = None

    @property
    def raw(self):
        return self._raw_value

    def parse(self, entity_id: str, value):
        """ Parse the function value to raw, selector or random """
        if str(value) == "__rand__":
            self.value_type = FunctionValueType.RANDOM

        if str(value).startswith("@"):
            self.value_type = FunctionValueType.SELECTOR
            self._selector_value = velvet_dawn.mechanics.selectors.get_selector(entity_id, value[1:])

        self._raw_value = value

        return self

    def value(self, instance):
        """ Get the value of the function value """
        if self.value_type == FunctionValueType.SELECTOR:
            return self._selector_value.function_get_value(instance)

        if self.value_type == FunctionValueType.RANDOM:
            return random.random()

        return self._raw_value
