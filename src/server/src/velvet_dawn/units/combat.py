import velvet_dawn
from velvet_dawn import errors, constants
from velvet_dawn.dao.models import Player
from velvet_dawn.db.instances import UnitInstance
from velvet_dawn.models.coordinate import Coordinate


def attack_entity(user: Player, attacker_id: str, attack_position: Coordinate):
    """ This function handles combat between one unit and all units in the target
    positions.

    This function will handle:
     - one unit against multiple units

    Args:
        user: The player trying to perform the action
        attacker_id: Instance id of the unit attacking
        attack_position: The position the unit is attacking
    """
    attacker = velvet_dawn.db.units.get_unit_by_instance_id(attacker_id)
    if not attacker:
        raise errors.ValidationError("Attacker ID does not exist")

    # TODO Check it is player's turn

    if not user or user.name != attacker.player:
        raise errors.ValidationError("You do not own this unit")

    attackees = velvet_dawn.db.units.get_units_at_positions(attack_position)
    if not attackees:
        raise errors.ValidationError("Not units found in this position")

    # Perform attack on all units in the position
    combat_damage = attacker.get_attribute("combat.attack", constants.UNIT_DEFAULT_COMBAT_ATTACK) / len(attackees)
    for attackee in attackees:
        # Both units attack each other but the attacks damange is shared across units
        damage_entity(attacker, attackee, combat_damage)
        damage_entity(attackee, attacker, attackee.get_attribute("combat.attack"))


# TODO Triggers
def damage_entity(attacker: UnitInstance, entity: UnitInstance, damage: float):
    new_health = entity.get_attribute("health", default=constants.UNIT_DEFAULT_HEALTH_MAX) - damage

    if new_health <= 0:
        # TODO Chat message saying '{player_name}'s {unit name} killed {player_names}'s {unit name}'
        velvet_dawn.units.kill(entity)

    else:
        entity.set_attribute("health", new_health)
