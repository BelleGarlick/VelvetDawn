import dataclasses
import random
from typing import List

import velvet_dawn
from velvet_dawn import errors
import velvet_dawn.map.neighbours
from velvet_dawn.models.datapacks.units.abilities import Ability


@dataclasses.dataclass
class NotActionable:
    ability_id: str
    reason: str

    def json(self):
        return {
            "abilityId": self.ability_id,
            "reason": self.reason
        }


class UnitAbilityData:
    def __init__(self):
        self.instance_id: int = -1
        self.hidden: List[NotActionable] = []
        self.disabled: List[NotActionable] = []
        self.abilities: List[str] = []

    def json(self):
        return {
            "instance": self.instance_id,
            "hidden": [x.json() for x in self.hidden],
            "disabled": [x.json() for x in self.disabled],
            "abilities": self.abilities,
        }


def run_unit_ability(player_name: str, unit_instance_id: str, ability_id: str):
    """ Verify ability a unit with the specified ability id

    Args:
        player_name: The player running the ability
        unit_instance_id: The unit instance
        ability_id: The ability id
    """
    instance = velvet_dawn.db.units.get_unit_by_instance_id(unit_instance_id)
    if not instance:
        raise errors.ValidationError("Unit not found.")

    unit = velvet_dawn.datapacks.entities.get(instance.entity_id)
    ability: Ability = unit.abilities.get_by_id(ability_id)

    if not ability:
        raise errors.ValidationError("Ability not found")

    if instance.player != player_name:
        raise errors.ValidationError("You do not own this unit.")

    # Check is not hidden
    is_hidden, reason = ability.is_hidden(instance)
    if is_hidden:
        raise errors.ValidationError(f"Cannot run ability. {reason}")

    # Check is not disabled
    is_enabled, reason = ability.is_enabled(instance)
    if is_enabled:
        raise errors.ValidationError(f"Cannot run ability. {reason}")

    ability.run(instance)


def get_unit_ability_updates(unit_instance_id: str):
    """ Get the breakdown of abilities that are hidden / disabled
     or already used """
    abilities = UnitAbilityData()

    instance = velvet_dawn.db.units.get_unit_by_instance_id(unit_instance_id)
    if not instance:
        return abilities

    unit_definition = velvet_dawn.datapacks.entities.get(instance.entity_id)
    if not unit_definition:
        return abilities

    # Iterate through all abilities to find which can/can't be run
    for ability in unit_definition.abilities.abilities:
        # Check if not hidden
        is_hidden, reason = ability.is_hidden(instance)
        if is_hidden:
            abilities.hidden.append(NotActionable(ability_id=ability.id, reason=reason))
            continue

        # Check if enabled
        is_enabled, reason = ability.is_enabled(instance)
        if is_enabled:
            abilities.disabled.append(NotActionable(ability_id=ability.id, reason=reason))
            continue

        abilities.abilities.append(ability.id)

    return abilities


def get_player_unit_abilities(player_name: str, full_list=False):
    """ Get a state update for a random unit / the full list of units.
    Continuously doing this overtime will result in eventual consistency
    without hammering the server constantly checking the abilities
    """
    units = velvet_dawn.units.list(player=player_name)

    if not units:
        return []

    if not full_list:
        units = [random.choice(units)]

    return [
        get_unit_ability_updates(unit.id)
        for unit in units
    ]
