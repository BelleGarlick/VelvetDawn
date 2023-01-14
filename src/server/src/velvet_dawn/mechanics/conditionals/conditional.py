import enum
from typing import Optional, Union

import velvet_dawn.validations
from velvet_dawn import errors
from velvet_dawn.dao.models import UnitInstance, TileInstance
from velvet_dawn.dao.models.world_instance import WorldInstance
from velvet_dawn.mechanics import selectors
from velvet_dawn.mechanics.function_value import FunctionValue
from velvet_dawn.mechanics.selectors import Selector


# Possible comparisons
class Comparison(enum.Enum):
    EQUALS = 0
    NOT_EQUALS = 1
    LESS_THAN = 2
    LESS_THAN_EQUAL = 3
    GREATER_THAN = 4
    GREATER_THAN_EQUAL = 5
    HAS_TAG = 6
    NOT_HAS_TAG = 7


# Comparison keys
OPERATORS = {
    "equals": Comparison.EQUALS, "eq": Comparison.EQUALS,
    "not-equals": Comparison.NOT_EQUALS, "ne": Comparison.NOT_EQUALS,
    "less-than": Comparison.LESS_THAN, "lt": Comparison.LESS_THAN,
    "less-than-equals": Comparison.LESS_THAN_EQUAL, "lte": Comparison.LESS_THAN_EQUAL,
    "greater-than": Comparison.GREATER_THAN, "gt": Comparison.GREATER_THAN,
    "greater-than-equals": Comparison.GREATER_THAN_EQUAL, "gte": Comparison.GREATER_THAN_EQUAL,
    "tagged": Comparison.HAS_TAG, "not-tagged": Comparison.NOT_HAS_TAG
}


# Numeric only operators
NUMBERS_ONLY_OPERATORS = {
    Comparison.LESS_THAN, Comparison.LESS_THAN_EQUAL, Comparison.GREATER_THAN_EQUAL, Comparison.GREATER_THAN
}


class Conditional:

    def __init__(self, keyword: str, has_tag_enabled=True):
        self.selector: Optional[Selector] = None
        self.function: Optional[Comparison] = None
        self.function_value = FunctionValue()

        self.keyword = keyword
        self.has_tag_enabled = has_tag_enabled

        self.not_true_reason = "A condition was not met."

    def load(self, id: str, data: dict):
        """ Parse the data into the conditional """
        self.selector = velvet_dawn.mechanics.selectors.get_selector(id, data[self.keyword])
        del data[self.keyword]

        if "notes" in data:
            del data["notes"]

        if "reason" in data:
            self.not_true_reason = data["reason"]
            del data['reason']

        for key in data:
            if key not in OPERATORS:
                raise errors.ValidationError(f"Invalid key in conditional: '{key}' in {id}.")

        if len(data) != 1:
            raise errors.ValidationError(f"Invalid operators in conditional: {data} in {id}. Conditionals must "
                                         f"contain only one operator.")

        # Test keys
        operator_key = list(data)[0]
        self.function = OPERATORS[operator_key]
        self.function_value.parse(id, data[operator_key])

        if self.function in NUMBERS_ONLY_OPERATORS:
            velvet_dawn.validations.is_int(self.function_value.raw, error_prefix=f"Conditional in {id} with operation '{operator_key}' comparison")

        if self.selector.attribute is not None and (self.function == Comparison.HAS_TAG or self.function == Comparison.NOT_HAS_TAG):
            raise errors.ValidationError(f"Cannot compare tags on this selector with an attribute on '{id}'.")
        if (self.function == Comparison.HAS_TAG or self.function == Comparison.NOT_HAS_TAG) and not self.has_tag_enabled:
            raise errors.ValidationError(f"Cannot compare tags using a '{self.keyword}' comparison method on '{id}'")

        return self

    def is_true(self, instance: Union[UnitInstance, TileInstance, WorldInstance]) -> bool:
        """ Call the conditional function """
        raise NotImplementedError()
