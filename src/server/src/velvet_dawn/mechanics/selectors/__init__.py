from typing import Optional

from velvet_dawn import errors

from .selector import Selector
from .selector_self import SelectorSelf
from .selector_world import SelectorWorld
from .selector_tiles import SelectorTile, SelectorTiles
from .selector_closest import (
    SelectorClosest,
    SelectorClosestEnemy,
    SelectorClosestFriendly
)
from .selector_commanders import (
    SelectorCommander,
    SelectorCommanders,
    SelectorFriendlyCommanders,
    SelectorEnemyCommanders
)
from .selector_units import (
    SelectorUnit,
    SelectorUnits,
    SelectorFriendlies,
    SelectorEnemies
)


""" Selectors module

This is the entry point to load a selectors module based on the 
selector string ('local[range=10].health.max'). The get_selector
function will load the suitable select for which the function
is called for. 
"""


SELECTORS = {
    selector.selector_name: selector
    for selector in [
        SelectorSelf(), SelectorWorld(), SelectorTile(), SelectorTiles(),
        SelectorClosest(), SelectorClosestEnemy(), SelectorClosestFriendly(),
        SelectorCommander(), SelectorCommanders(), SelectorFriendlyCommanders(), SelectorEnemyCommanders(),
        SelectorUnit(), SelectorUnits(), SelectorFriendlies(), SelectorEnemies()
    ]
}


# todo more documenation and testing
def get_selector(entity_id: str, selector_string: str) -> Selector:
    """ Parse a selector string.

    This works by separating out the chains, setting the
    tags and setting the attributes

    Args:
        entity_id: Shown to the user if an error is raised
        selector_string: String to parse

    Returns:
        The parsed selector.
    """
    selector_string = selector_string.replace(" ", "")

    head: Optional[Selector] = None
    last: Optional[Selector] = None

    for chain in selector_string.split(">"):
        # Parse the selectors
        if "[" in chain:
            selector_name, filters_and_attributes = chain.split("[")
            filters, attribute = filters_and_attributes.split("]")
            attribute = attribute[1:]
            filters = filters.replace(" ", "").split(",") if filters else None

        else:
            tokens = chain.split(".")
            filters = None
            selector_name = tokens[0]
            attribute = ".".join(tokens[1:])

        # Load selector for the given type
        selector = SELECTORS.get(selector_name)
        if not selector:
            raise errors.ValidationError(f"Selector '{selector_name}' cannot be used on '{entity_id}'")

        selector = selector.instantiate(selector_string, filters, attribute if attribute else None)

        if head is None: head = selector
        if last is not None: last.chained_selector = selector
        last = selector

        head.attribute = attribute if attribute else None

    if head is None:
        raise errors.ValidationError(f"Problem with selector '{selector_string}' detected.")

    return head
