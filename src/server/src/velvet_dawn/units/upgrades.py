import dataclasses
import random
from typing import List

import velvet_dawn
from velvet_dawn import errors
import velvet_dawn.map.neighbours
from velvet_dawn.dao import db
from velvet_dawn.dao.models.upgrades import UnitUpgrade
from velvet_dawn.models.datapacks.units.upgrades import Upgrade


@dataclasses.dataclass
class NotUpgradable:
    upgrade_id: str
    reason: str

    def json(self):
        return {
            "upgradeId": self.upgrade_id,
            "reason": self.reason
        }


class UnitUpgradeData:
    def __init__(self):
        self.instance_id: int = -1
        self.upgraded: List[str] = []
        self.hidden: List[NotUpgradable] = []
        self.disabled: List[NotUpgradable] = []
        self.upgrades: List[str] = []
        self.missing_requirements: List[NotUpgradable] = []

    def json(self):
        return {
            "instance": self.instance_id,
            "upgraded": self.upgraded,
            "hidden": [x.json() for x in self.hidden],
            "disabled": [x.json() for x in self.disabled],
            "missingRequirements": [x.json() for x in self.missing_requirements],
            "upgrades": self.upgrades,
        }


def upgrade_unit(player_name: str, unit_instance_id: str, upgrade_id: str):
    """ Verify upgrade a unit with the specified upgrade id

    Args:
        player_name: The player running the upgrade
        unit_instance_id: The unit instance
        upgrade_id: The upgrade id
    """
    instance = velvet_dawn.db.units.get_unit_by_instance_id(unit_instance_id)
    if not instance:
        raise errors.ValidationError("Unit not found.")

    unit = velvet_dawn.datapacks.entities.get(instance.entity_id)
    upgrade: Upgrade = unit.upgrades.get_by_id(upgrade_id)

    if not upgrade:
        raise errors.ValidationError("Upgrade not found")

    if instance.player != player_name:
        raise errors.ValidationError("You do not own this unit.")

    if db.session.query(UnitUpgrade).where(
            UnitUpgrade.instance_id==unit_instance_id,
            UnitUpgrade.upgrade_id==upgrade_id
    ).one_or_none():
        raise errors.ValidationError("Unit already has this upgrade.")

    unit_existing_upgrades = {
        x.upgrade_id for x in db.session.query(UnitUpgrade).where(
            UnitUpgrade.instance_id==unit_instance_id).all()
    }

    # Test for missing requirments
    missing_requirements = list(filter(lambda x: x not in unit_existing_upgrades, upgrade.requires))
    if missing_requirements:
        requirement = unit.upgrades.get_by_id(missing_requirements[0])
        requirement_name = requirement.name if requirement else missing_requirements[0]
        raise errors.ValidationError(f"Requires: '{requirement_name}'")

    # Check is not hidden
    is_hidden, reason = upgrade.is_hidden(instance)
    if is_hidden:
        raise errors.ValidationError(f"Cannot run upgrade. {reason}")

    # Check is not disabled
    is_enabled, reason = upgrade.is_enabled(instance)
    if not is_enabled:
        raise errors.ValidationError(f"Cannot run upgrade. {reason}")

    # Run the upgrade
    db.session.add(UnitUpgrade(instance_id=unit_instance_id, upgrade_id=upgrade_id))
    db.session.commit()
    upgrade.run(instance)


def get_unit_upgrade_updates(unit_instance_id: str):
    """ Get the breakdown of upgrades that are hidden / disabled
     or already used """
    upgrades = UnitUpgradeData()

    instance = velvet_dawn.db.units.get_unit_by_instance_id(unit_instance_id)
    if not instance:
        return upgrades

    unit_definition = velvet_dawn.datapacks.entities.get(instance.entity_id)
    if not unit_definition:
        return upgrades

    unit_existing_upgrades = {
        x.upgrade_id for x in db.session.query(UnitUpgrade).where(
            UnitUpgrade.instance_id==unit_instance_id).all()
    }

    # Iterate through all upgrades to find which can/can't be run
    for upgrade in unit_definition.upgrades.upgrades:
        if upgrade.id in unit_existing_upgrades:
            upgrades.upgraded.append(upgrade.id)
            continue

        # Check if all requirements are upgraded
        missing_requirements = list(filter(lambda x: x not in unit_existing_upgrades, upgrade.requires))
        if missing_requirements:
            requirement = unit_definition.upgrades.get_by_id(missing_requirements[0])
            requirement_name = requirement.name if requirement else missing_requirements[0]

            upgrades.missing_requirements.append(NotUpgradable(
                upgrade_id=upgrade.id, reason=f"Requires: '{requirement_name}'"))
            continue

        # Check if not hidden
        is_hidden, reason = upgrade.is_hidden(instance)
        if is_hidden:
            upgrades.hidden.append(NotUpgradable(upgrade_id=upgrade.id, reason=reason))
            continue

        # Check if enabled
        is_enabled, reason = upgrade.is_enabled(instance)
        if not is_enabled:
            upgrades.disabled.append(NotUpgradable(upgrade_id=upgrade.id, reason=reason))
            continue

        upgrades.upgrades.append(upgrade.id)

    return upgrades


def get_player_unit_upgrades(player_name: str, full_list=False):
    """ Get a state update for a random unit / the full list of units.
    Continuously doing this overtime will result in eventual consistency
    without hammering the server constantly checking the upgrades
    """
    units = velvet_dawn.units.list(player=player_name)

    if not units:
        return []

    if not full_list:
        units = [random.choice(units)]

    return [
        get_unit_upgrade_updates(unit.id)
        for unit in units
    ]
