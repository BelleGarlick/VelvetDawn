import velvet_dawn.mechanics.conditionals
from velvet_dawn import errors
from velvet_dawn.mechanics.actions.action import Action
from velvet_dawn.mechanics.actions.action_modify import ActionModify


""" This module is the entry point for getting an action given a string.
The class will be chosen based on keys in the dict then return the parsed
action based on the dict.

Examples:
    {"if": [...], "modify": "self.health", "set": 5} -> set the health of the unit to 5
"""


def get_action(id: str, data: dict) -> Action:
    """ Given the dict, decide which action class should be used

    Args:
        id: The id of the entity attached to this action
        data: The dictionary defining which action should be used

    Returns:
        The chosen action object
    """
    if not isinstance(data, dict):
        raise errors.ValidationError(f"Invalid actionable in {id}. '{data}' must be a dictionary")

    built_action = None
    if "modify" in data:
        built_action = ActionModify.from_dict(id, data)

    # Create the comparison objects
    conditions = data.get("conditions", [])
    for condition in conditions:
        built_action.conditions.append(velvet_dawn.mechanics.conditionals.get_conditional(id, condition))

    if not built_action:
        raise errors.ValidationError(f"Invalid action '{data}' on {id}")

    return built_action
