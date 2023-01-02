from typing import Dict, Type, Union

from velvet_dawn import errors
from velvet_dawn.models.datapacks.unit import Unit
from velvet_dawn.models.datapacks.tiles import Tile
from .selector import Selector, SelectorParentType
from .selector_self import SelectorSelf
from .selector_local import (
    SelectorLocal,
    SelectorLocalUnits,
    SelectorLocalEnemies,
    SelectorLocalFriendlies,
    SelectorLocalTiles
)
from .selector_tile import SelectorTile
from .selector_unit import SelectorUnit


""" Selectors module

This is the entry point to load a selectors module based on the 
selector string ('local[range=10].health.max'). The get_selector
function will load the suitable select for which the function
is called for. 
"""


SELECTORS = [
    SelectorSelf(), SelectorLocal(), SelectorLocalUnits(), SelectorLocalEnemies(), SelectorLocalFriendlies(),
    SelectorLocalTiles(), SelectorTile(), SelectorUnit()
]

TILE_SELECTOR_MAP: Dict[str, Selector] = {
    selector.selector_name: selector
    for selector in SELECTORS
    if selector.parent_type in {SelectorParentType.ANY, SelectorParentType.TILE}
}

UNIT_SELECTOR_MAP: Dict[str, Selector] = {
    selector.selector_name: selector
    for selector in SELECTORS
    if selector.parent_type in {SelectorParentType.ANY, SelectorParentType.UNIT}
}


def get_selector(entity_id: str, parent_type: Union[Type[Unit], Type[Tile]], selector_string: str) -> Selector:
    """ Get selector for the given parent_type

    Args:
        entity_id: Shown to the user if an error is raised
        parent_type: The type to load for
        selector_string: String to parse

    Returns:
        The parsed selector.
    """
    # TODO Use regex to check in correct format
    # Parse the selectors
    if "[" in selector_string:
        selector_name, filters_and_attributes = selector_string.split("[")
        filters, attribute = filters_and_attributes.split("]")
        attribute = attribute[1:]
        filters = filters.replace(" ", "").split(",") if filters else None

    else:
        tokens = selector_string.split(".")
        filters = None
        selector_name = tokens[0]
        attribute = ".".join(tokens[1:])

    # Load selector for the given type
    selector = None
    if parent_type == Unit:
        selector = UNIT_SELECTOR_MAP.get(selector_name)
    if parent_type == Tile:
        selector = TILE_SELECTOR_MAP.get(selector_name)

    if not selector:
        raise errors.ValidationError(f"Selector '{selector_name}' cannot be used on '{entity_id}'")

    return selector.instantiate(selector_string, filters, attribute if attribute else None)
