from typing import Union, Type

from velvet_dawn import errors
from velvet_dawn.mechanics.actions.action import Action
from velvet_dawn.mechanics.actions.action_modify import ActionModify
from velvet_dawn.models import Unit, Tile

""" This module is the entry point for getting an action given a string.
The class will be chosen based on keys in the dict then return the parsed
action based on the dict.

Examples:
    {"if": [...], "modify": "self.health", "set": 5} -> set the health of the unit to 5
"""


def get_action(id: str, parent_type: Union[Type[Unit], Type[Tile]], data: dict) -> Action:
    """ Given the dict, decide which action class should be used

    Args:
        id: The id of the entity attached to this action
        parent_type: The type of the entity attached to this action
        data: The dictionary defining which action should be used

    Returns:
        The chosen action object
    """
    if not isinstance(data, dict):
        raise errors.ValidationError(f"Invalid actionable in {id}. '{data}' must be a dictionary")

    if "modify" in data:
        return ActionModify.from_dict(id, parent_type, data)

    else:
        raise errors.ValidationError(f"Invalid action '{data}' on {id}")
