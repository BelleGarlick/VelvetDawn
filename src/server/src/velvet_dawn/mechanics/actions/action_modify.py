import enum
from typing import Union, Type, Optional

import velvet_dawn.mechanics.selectors
from velvet_dawn import errors
from velvet_dawn.config import Config
from velvet_dawn.dao.models import TileInstance, UnitInstance
from velvet_dawn.mechanics.actions.action import Action
from velvet_dawn.mechanics.selectors import Selector
from velvet_dawn.models import Unit, Tile


""" The action modify class, responsible for modifying 
attributes of selector attached.
"""


class ActionModifierFunction(enum.Enum):
    """ Possible actions """
    SET = 0
    ADD = 1
    SUB = 2
    MUL = 3


""" The key:function map defined in the datapack dictionary """
KeyMap = {
    "set": ActionModifierFunction.SET,
    "add": ActionModifierFunction.ADD,
    "sub": ActionModifierFunction.SUB,
    "subtract": ActionModifierFunction.SUB,
    "mul": ActionModifierFunction.MUL,
    "multiply": ActionModifierFunction.MUL,
}


class ActionModify(Action):

    def __init__(self):
        super().__init__()

        self.selector: Optional[Selector] = None

        self.function: ActionModifierFunction = ActionModifierFunction.SET
        self.function_value = 0

    @staticmethod
    def from_dict(id: str, parent_type: Union[Type[Unit], Type[Tile]], data: dict):
        """ Parse the dict of tile/unit data to construct this action """
        if 'modify' not in data:
            raise errors.ValidationError("Modify functions must contain a 'modify' selector")

        # Check the number of functions is valid
        total_function_keys = sum([1 for key in data if key in KeyMap])
        if total_function_keys != 1:
            raise errors.ValidationError(f"Invalid modify action on {id}. Modify actions must contain one of {list(KeyMap)}.")

        # Construct the action and it's function
        action = ActionModify()
        # TODO Conditions
        action.selector = velvet_dawn.mechanics.selectors.get_selector(id, parent_type, data['modify'])

        if action.selector.attribute is None:
            raise errors.ValidationError(
                f"Modify actions must ensure the selectors modify an attribute not '{data['modify']}")

        for key in data:
            if key in KeyMap:
                action.function_value = data[key]
                action.function = KeyMap[key]

        return action

    def run(self, instance: Union[TileInstance, UnitInstance], config: Config):
        """ Execute the attribute """
        if self.function == ActionModifierFunction.SET:
            self.selector.function_set(instance, self.function_value, config)

        elif self.function == ActionModifierFunction.ADD:
            self.selector.function_add(instance, self.function_value, config)

        elif self.function == ActionModifierFunction.MUL:
            self.selector.function_multiply(instance, self.function_value, config)

        elif self.function == ActionModifierFunction.SUB:
            self.selector.function_subtract(instance, self.function_value, config)

        else:
            raise errors.ValidationError(f"Unknown action function type: '{self.function}'")