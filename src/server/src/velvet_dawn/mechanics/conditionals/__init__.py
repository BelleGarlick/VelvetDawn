from velvet_dawn import errors
from velvet_dawn.mechanics.conditionals.conditional_counting import ConditionalCounting
from velvet_dawn.mechanics.conditionals.conditional_standard import ConditionalStandard


def get_conditional(entity_id: str, data: dict):
    """ Load the correct conditional class given the dict

    Args:
        entity_id: The entity the condition is being attached to.
        data: The dictionary of information.
    """
    if not isinstance(data, dict):
        raise errors.ValidationError(f"Conditional items must be a dictionary not '{data}' in {id}")

    if "if" in data:
        return ConditionalStandard().load(entity_id, data)
    elif "count" in data:
        return ConditionalCounting().load(entity_id, data)

    raise errors.ValidationError(f"Unknown conditional operation '{data}'. Please see datapack documentation.")
