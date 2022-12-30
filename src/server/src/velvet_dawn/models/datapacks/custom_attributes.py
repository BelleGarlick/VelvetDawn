import re
from typing import List

import velvet_dawn
from velvet_dawn import errors
from velvet_dawn.logger import logger


""" Custom Attributes

Custom attributes may be applied to a tile or entity
to allow for custom values to be stored and modified
in game. 
"""


# No icon defined will use this id. This will give a pink texture
# letting the user know the texture is missing
EMPTY_ICON_TAG = "__empty__"

AVAILABLE_KEYS = {"id", "name", "icon", "default", "hidden", "notes"}


class CustomAttribute:

    def __init__(self):
        self.id = None
        self.name = None
        self.default = 0
        self.icon = None
        self.hidden = False

    def json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "default": self.default,
            "icon": self.icon,
            "hidden": self.hidden
        }

    @staticmethod
    def load(parent_id: str, data: dict):
        if not isinstance(data, dict):
            raise errors.ValidationError(f"Object '{parent_id}' invalid attribute. Attributes must be json objects.")

        custom_attribute = CustomAttribute()
        custom_attribute.id = data.get("id")
        custom_attribute.name = data.get("name")
        custom_attribute.default = data.get("default", 0)
        custom_attribute.icon = data.get("icon", EMPTY_ICON_TAG)
        custom_attribute.hidden = data.get("hidden", False)

        # Validate attribute id
        if not isinstance(custom_attribute.id, str):
            raise errors.ValidationError(f"Object '{parent_id}' attribute id '{custom_attribute.id}' is not valid. Must be a string.")
        if not re.fullmatch(r'[a-z][a-z0-9-]{0,32}', custom_attribute.id):
            raise errors.ValidationError(f"Object '{parent_id}' attribute id '{custom_attribute.id}' is not valid. Id must be at least 1 and smaller than 33 chars long and contain only letters, numbers or hyphens and begin in a letter. All letters must be lowercase.")

        # Validate attribute name
        if not isinstance(custom_attribute.name, str):
            raise errors.ValidationError(
                f"Object '{parent_id}' attribute name '{custom_attribute.name}' is not valid. Must be a string.")
        if not re.fullmatch(r'[a-zA-Z0-9 ]{1,32}', custom_attribute.name):
            raise errors.ValidationError(
                f"Object '{parent_id}' attribute name '{custom_attribute.name}' is not valid. Id must be at least 1 and smaller than 33 chars long and contain only letters or numbers.")

        # Validate attribute default
        if not isinstance(custom_attribute.default, float) and not isinstance(custom_attribute.default, int):
            raise errors.ValidationError(
                f"Object '{parent_id}' attribute '{custom_attribute.id}' default value is not valid. Must be a number.")

        # Validate attribute icon
        if not isinstance(custom_attribute.icon, str):
            raise errors.ValidationError(
                f"Object '{parent_id}' attribute '{custom_attribute.id}' icon is not valid. Must be a string.")
        if custom_attribute.icon not in velvet_dawn.datapacks.resources and custom_attribute.icon is not EMPTY_ICON_TAG:
            logger.warning(
                f"Object '{parent_id}' attribute '{custom_attribute.id}' icon is not valid. Resource '{custom_attribute.icon}' not found.")

        # Validate attribute hidden
        if not isinstance(custom_attribute.hidden, bool):
            raise errors.ValidationError(
                f"Object '{parent_id}' attribute '{custom_attribute.id}' hidden value is not valid. Must be a bool.")

        # Check for random other keys
        for key in data:
            if key not in AVAILABLE_KEYS:
                raise errors.ValidationError(f"{parent_id} attribute's has unknown key: '{key}'")

        return custom_attribute


class CustomAttributes:

    def __init__(self):
        self.attributes: List[CustomAttribute] = []

    def json(self):
        """ Get the json returned in the object definition """
        return [x.json() for x in self.attributes]

    def db_json(self):
        """ Return values in a dict mapping the attr. id to the value """
        return {x.id: x.default for x in self.attributes}

    @staticmethod
    def load(parent_id: str, items: list):
        """ Parse the data to create the attributes """
        if not isinstance(items, list):
            raise errors.ValidationError(f"Object '{parent_id}' attributes are invalid. Must be a list of json objects.")

        custom_attributes = CustomAttributes()
        custom_attributes.attributes = [
            CustomAttribute.load(parent_id, x)
            for x in items
        ]

        # Validate attributes, check for duplicate ids
        ids = set()
        for item in custom_attributes.attributes:
            if item.id in ids:
                raise errors.ValidationError(f"Object '{parent_id}' has duplicated attribute id '{item.id}'")
            ids.add(item.id)

        return custom_attributes
