from typing import List, Tuple

import velvet_dawn.mechanics.conditionals
from velvet_dawn import errors
from velvet_dawn.dao.models import UnitInstance
from velvet_dawn.logger import logger
from velvet_dawn.mechanics.actions import Action
from velvet_dawn.mechanics.conditionals.conditional import Conditional


VALID_KEYS = {"id", "name", "enabled", "requires", "actions", "icon", "hidden", "notes", "description"}


class Upgrade:
    def __init__(self):
        self.id: str = ""
        self.name: str = ""
        self.icon: str = ""
        self.description: str = ""

        self.enabled: List[Conditional] = []
        self.hidden: List[Conditional] = []
        self.actions: List[Action] = []

        self.requires: List[str] = []

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "icon": self.icon,
            "requires": self.requires,
            "description": self.description
        }

    @staticmethod
    def load(parent_id: str, upgrade_number: int, data: dict):
        """ Load the upgrade json

        Args:
            parent_id: The id of the parent the upgrade is for, used
                in error messages.
            upgrade_number: The index which this upgrade is within the
                list of upgrades in the parent object. Used to form an
                id if not specified.
            data: The data the object loads from

        Returns:
            The parsed object
        """
        upgrade = Upgrade()

        # Parse id
        upgrade.id = data.get("id", f"{parent_id}-upgrade-{upgrade_number}")
        if not isinstance(upgrade.id, str):
            raise errors.ValidationError(f"Upgrade id '{data.get('id')}' is invalid.")

        # Parse name
        upgrade.name = str(data.get("name"))
        if not isinstance(data.get("name"), str):
            raise errors.ValidationError(f"Upgrade name '{data.get('name')}' is invalid.")

        # Parse description
        upgrade.description = str(data.get("description", ""))
        if not isinstance(upgrade.description, str):
            raise errors.ValidationError(f"Upgrade description '{data.get('description')}' is invalid.")

        # Parse icons
        upgrade.icon = data.get("icon")
        if upgrade.icon is None:
            logger.warning(
                f"Upgrade '{parent_id}' has an upgrade with a missing icon ({upgrade.icon}).")

        elif upgrade.icon not in velvet_dawn.datapacks.resources:
            logger.warning(
                f"Upgrade '{parent_id}' icon '{upgrade.icon}' icon is not valid. Resource '{upgrade.icon}' not found.")

        # Parse enabled conditions
        enabled_conditions = data.get("enabled", [])
        if not isinstance(enabled_conditions, list):
            raise errors.ValidationError(f"Upgrade enabled in {parent_id} is invalid. Enabled attributes must be a "
                                         f"list of conditions.")
        upgrade.enabled = [
            velvet_dawn.mechanics.conditionals.get_conditional(parent_id, item)
            for item in enabled_conditions
        ]

        # Parse hidden conditions
        hidden_conditions = data.get("hidden", [])
        if not isinstance(hidden_conditions, list):
            raise errors.ValidationError(f"Upgrade hidden in {parent_id} is invalid. Hidden attributes must be a list "
                                         f"of conditions.")
        upgrade.hidden = [
            velvet_dawn.mechanics.conditionals.get_conditional(parent_id, item)
            for item in hidden_conditions
        ]

        # Parse actions
        upgrade_actions = data.get("actions", [])
        if not isinstance(upgrade_actions, list):
            raise errors.ValidationError(f"Upgrade actions in {parent_id} is invalid. Actions attributes must be a "
                                         f"list of actions.")
        upgrade.actions = [
            velvet_dawn.mechanics.actions.get_action(parent_id, item)
            for item in upgrade_actions
        ]

        upgrade.requires = data.get("requires", [])
        if not isinstance(upgrade.requires, list):
            raise errors.ValidationError(
                f"Upgrade requirements (in {parent_id}) must be a list. Found '{upgrade.requires}'.")
        for item in upgrade.requires:
            if not isinstance(item, str):
                raise errors.ValidationError(f"Upgrade requirement '{item}' (in {parent_id}) must be a string.")

        # check invalid key
        for key in data:
            if key not in VALID_KEYS:
                raise errors.ValidationError(f"Invalid upgrade key '{key}' (in {parent_id})")

        return upgrade

    def run(self, instance: UnitInstance):
        """ Execute the upgrade """
        for action in self.actions:
            action.run(instance)

    def is_hidden(self, instance: UnitInstance) -> Tuple[bool, str]:
        """ Check if the upgrade should be hidden and therefore not ran """
        for condition in self.hidden:
            if condition.is_true(instance):
                return True, condition.not_true_reason
        return False, ""

    def is_enabled(self, instance: UnitInstance) -> Tuple[bool, str]:
        """ Check if the upgrade should be disabled and therefore not ran """
        for condition in self.enabled:
            if not condition.is_true(instance):
                return False, condition.not_true_reason
        return True, ""


class Upgrades:
    def __init__(self):
        self.upgrades: List[Upgrade] = []
        self.__upgrades_by_id = {}

    def get_by_id(self, upgrade_id: str):
        """ Get an upgrade from it's id """
        return self.__upgrades_by_id.get(upgrade_id)

    def json(self):
        return [
            upgrade.json()
            for upgrade in self.upgrades
        ]

    def load(self, parent_id: str, data: list):
        """ Parse the upgrades list """
        if not isinstance(data, list):
            raise errors.ValidationError(f"Upgrades must be a list. Found {data} in {parent_id}")

        self.upgrades = [
            Upgrade.load(parent_id, upgrade_id, upgrade_data)
            for upgrade_id, upgrade_data in enumerate(data)
        ]
        self.__upgrades_by_id = {
            upgrade.id: upgrade
            for upgrade in self.upgrades
        }
