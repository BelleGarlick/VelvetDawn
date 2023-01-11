from typing import List, Tuple

import velvet_dawn.mechanics.conditionals
from velvet_dawn import errors
from velvet_dawn.dao.models import UnitInstance
from velvet_dawn.logger import logger
from velvet_dawn.mechanics.actions import Action
from velvet_dawn.mechanics.conditionals.conditional import Conditional


VALID_KEYS = {"name", "enabled", "actions", "hidden", "icon", "notes", "description"}


class Ability:
    def __init__(self):
        self.id: str = ""
        self.name: str = ""
        self.icon: str = ""
        self.description: str = ""

        self.enabled: List[Conditional] = []
        self.hidden: List[Conditional] = []
        self.actions: List[Action] = []

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "icon": self.icon,
            "description": self.description
        }

    @staticmethod
    def load(parent_id: str, ability_number: int, data: dict):
        """ Load the ability json

        Args:
            parent_id: The id of the parent the ability is for, used
                in error messages.
            ability_number: The index which this ability is within the
                list of abilities in the parent object. Used to form an
                id if not specified.
            data: The data the object loads from

        Returns:
            The parsed object
        """
        ability = Ability()

        # Parse id
        ability.id = f"{parent_id}-ability-{ability_number}"

        # Parse name
        ability.name = str(data.get("name"))
        if not isinstance(data.get("name"), str):
            raise errors.ValidationError(f"Ability name '{data.get('name')}' is invalid.")

        # Parse description
        ability.description = str(data.get("description", ""))
        if not isinstance(ability.description, str):
            raise errors.ValidationError(f"Ability description '{data.get('description')}' is invalid.")

        # Parse icons
        ability.icon = data.get("icon")
        if ability.icon is None:
            logger.warning(
                f"Ability '{parent_id}' has an ability with a missing icon.")

        elif ability.icon not in velvet_dawn.datapacks.resources:
            logger.warning(
                f"Ability '{parent_id}' icon '{ability.icon}' icon is not valid. Resource '{ability.icon}' not found.")

        # Parse enabled conditions
        enabled_conditions = data.get("enabled", [])
        if not isinstance(enabled_conditions, list):
            raise errors.ValidationError(f"Ability enabled in {parent_id} is invalid. Enabled attributes must be a "
                                         f"list of conditions.")
        ability.enabled = [
            velvet_dawn.mechanics.conditionals.get_conditional(parent_id, item)
            for item in enabled_conditions
        ]

        # Parse hidden conditions
        hidden_conditions = data.get("hidden", [])
        if not isinstance(hidden_conditions, list):
            raise errors.ValidationError(f"Ability hidden in {parent_id} is invalid. Hidden attributes must be a list "
                                         f"of conditions.")
        ability.hidden = [
            velvet_dawn.mechanics.conditionals.get_conditional(parent_id, item)
            for item in hidden_conditions
        ]

        # Parse actions
        ability_actions = data.get("actions", [])
        if not isinstance(ability_actions, list):
            raise errors.ValidationError(f"Ability actions in {parent_id} is invalid. Actions attributes must be a "
                                         f"list of actions.")
        ability.actions = [
            velvet_dawn.mechanics.actions.get_action(parent_id, item)
            for item in ability_actions
        ]

        # check invalid key
        for key in data:
            if key not in VALID_KEYS:
                raise errors.ValidationError(f"Invalid ability key '{key}' (in {parent_id})")

        return ability

    def run(self, instance: UnitInstance):
        """ Execute the ability """
        for action in self.actions:
            action.run(instance)

    def is_hidden(self, instance: UnitInstance) -> Tuple[bool, str]:
        """ Check if the ability should be hidden and therefore not ran """
        for condition in self.hidden:
            if condition.is_true(instance):
                return True, condition.not_true_reason
        return False, ""

    def is_enabled(self, instance: UnitInstance) -> Tuple[bool, str]:
        """ Check if the ability should be disabled and therefore not ran """
        for condition in self.enabled:
            if not condition.is_true(instance):
                return True, condition.not_true_reason
        return False, ""


class Abilities:

    def __init__(self):
        self.abilities: List[Ability] = []
        self.__abilities_by_id = {}

    def get_by_id(self, ability_id: str):
        """ Get an ability from its id """
        return self.__abilities_by_id.get(ability_id)

    def json(self):
        return [
            abilty.json()
            for abilty in self.abilities
        ]

    def load(self, parent_id: str, data: list):
        """ Parse the abilities list """
        if not isinstance(data, list):
            raise errors.ValidationError(f"Abilities must be a list. Found {data} in {parent_id}")

        self.abilities = [
            Ability.load(parent_id, ability_id, ability_data)
            for ability_id, ability_data in enumerate(data)
        ]
        self.__abilities_by_id = {
            abilty.id: abilty
            for abilty in self.abilities
        }
