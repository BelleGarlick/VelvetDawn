import enum
from typing import Union, Optional

import velvet_dawn.mechanics.selectors
from velvet_dawn import errors
from velvet_dawn.dao.models import TileInstance, UnitInstance
from velvet_dawn.dao.models.world_instance import WorldInstance
from velvet_dawn.mechanics.actions.action import Action
from velvet_dawn.mechanics.function_value import FunctionValue
from velvet_dawn.mechanics.selectors import Selector


""" The action modify class, responsible for modifying 
attributes of selector attached.
"""


class ActionModifierFunction(enum.Enum):
    """ Possible actions """
    SET = 0
    ADD = 1
    SUB = 2
    MUL = 3
    RESET = 4

    ADD_TAG = 5
    REMOVE_TAG = 6


""" The key:function map defined in the datapack dictionary """
KeyMap = {
    "set": ActionModifierFunction.SET,
    "add": ActionModifierFunction.ADD,
    "sub": ActionModifierFunction.SUB,
    "subtract": ActionModifierFunction.SUB,
    "mul": ActionModifierFunction.MUL,
    "multiply": ActionModifierFunction.MUL,
    "reset": ActionModifierFunction.RESET,
    "add-tag": ActionModifierFunction.ADD_TAG,
    "remove-tag": ActionModifierFunction.REMOVE_TAG,

    "set-selector": ActionModifierFunction.SET,
    "add-selector": ActionModifierFunction.SET,
    "sub-selector": ActionModifierFunction.SET,
    "subtract-selector": ActionModifierFunction.SET,
    "mul-selector": ActionModifierFunction.SET,
    "multiply-selector": ActionModifierFunction.SET,
}


NON_ATTRIBUTE_MODIFIERS = {ActionModifierFunction.ADD_TAG, ActionModifierFunction.REMOVE_TAG}


class ActionModify(Action):

    def __init__(self):
        super().__init__()

        self.selector: Optional[Selector] = None

        self.function: ActionModifierFunction = ActionModifierFunction.SET
        self.function_value = FunctionValue()
        self.is_value_selector = False

    @staticmethod
    def from_dict(id: str, data: dict):
        """ Parse the dict of tile/unit data to construct this action """
        if 'modify' not in data:
            raise errors.ValidationError("Modify functions must contain a 'modify' selector")

        # Check the number of functions is valid
        total_function_keys = sum([1 for key in data if key in KeyMap])
        if total_function_keys != 1:
            raise errors.ValidationError(f"Invalid modify action on {id}. Modify actions must contain one of {list(KeyMap)}. Problem data: {data}")

        # Construct the action and it's function
        action = ActionModify()
        action.selector = velvet_dawn.mechanics.selectors.get_selector(id, data['modify'])

        # Find the key used and update the function (we already verify there is a key above)
        function_key = None
        for key in data:
            if key in KeyMap:
                function_key = key
                action.function_value.parse(id, data[key])
                action.function = KeyMap[key]

        if action.function in NON_ATTRIBUTE_MODIFIERS:
            if action.selector.attribute is not None:
                raise errors.ValidationError(
                    f"Action '{function_key}' tags cannot be performed on a selector with attributes '{data['modify']}")
        else:
            if action.selector.attribute is None:
                raise errors.ValidationError(
                    f"Modify actions must ensure the selectors modify an attribute not '{data['modify']}'")

        return action

    def run(self, instance: Union[TileInstance, UnitInstance, WorldInstance]):
        """ Execute the attribute """
        if self.function == ActionModifierFunction.SET:
            self.selector.function_set(instance, self.function_value.value(instance))

        elif self.function == ActionModifierFunction.ADD:
            self.selector.function_add(instance, self.function_value.value(instance))

        elif self.function == ActionModifierFunction.MUL:
            self.selector.function_multiply(instance, self.function_value.value(instance))

        elif self.function == ActionModifierFunction.SUB:
            self.selector.function_subtract(instance, self.function_value.value(instance))

        elif self.function == ActionModifierFunction.RESET:
            self.selector.function_reset(instance, self.function_value.value(instance))

        elif self.function == ActionModifierFunction.ADD_TAG:
            self.selector.function_add_tag(instance, self.function_value.value(instance))

        elif self.function == ActionModifierFunction.REMOVE_TAG:
            self.selector.function_remove_tag(instance, self.function_value.value(instance))

        else:
            raise errors.ValidationError(f"Unknown action function type: '{self.function}'")
