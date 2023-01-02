import re
from typing import Dict, Optional, Union

import velvet_dawn
from velvet_dawn import errors
from velvet_dawn.dao import db
from velvet_dawn.dao.models import UnitInstance
from velvet_dawn.logger import logger


# TODO Update documentation, wiki and tests


""" Custom Attributes

Custom attributes may be applied to a tile or entity to allow for custom 
values to be stored and modified in game. The datapacks allow users to 
define attributes, though this is mainly for allow a default value and 
ui element, attributes may be modified on the fly via functions.
"""


# No icon defined will use this id. This will give a pink texture
# letting the user know the texture is missing
EMPTY_ICON_TAG = "__empty__"

AVAILABLE_KEYS = {"id", "name", "icon", "default", "notes"}


class Attribute:

    def __init__(self):
        self.id = None
        self.name = None
        self.default = 0
        self.icon = None

    def json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "default": self.default,
            "icon": self.icon
        }

    @staticmethod
    def load(parent_id: str, data: dict):
        if not isinstance(data, dict):
            raise errors.ValidationError(f"Object '{parent_id}' invalid attribute. Attributes must be json objects.")

        for key in data:
            if key not in AVAILABLE_KEYS:
                raise errors.ValidationError(f"{parent_id} attribute's has unknown key: '{key}'")

        custom_attribute = Attribute()
        custom_attribute.id = data.get("id")
        custom_attribute.name = data.get("name")
        custom_attribute.default = data.get("default", 0)
        custom_attribute.icon = data.get("icon", EMPTY_ICON_TAG)

        # Validate attribute id
        if not isinstance(custom_attribute.id, str):
            raise errors.ValidationError(f"Object '{parent_id}' attribute id '{custom_attribute.id}' is not valid. Must be a string.")
        if not re.fullmatch(r'[a-z][a-z0-9-]{0,32}', custom_attribute.id):
            raise errors.ValidationError(f"Object '{parent_id}' attribute id '{custom_attribute.id}' is not valid. Id must be at least 1 and smaller than 33 chars long and contain only letters, numbers or hyphens and begin in a letter. All letters must be lowercase.")

        # Validate attribute name
        if custom_attribute.name is not None:
            if not isinstance(custom_attribute.name, str):
                raise errors.ValidationError(
                    f"Object '{parent_id}' attribute name '{custom_attribute.name}' is not valid. Must be a string.")
            if not re.fullmatch(r'[a-zA-Z0-9. ]{1,32}', custom_attribute.name):
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

        return custom_attribute


class Attributes:

    def __init__(self):
        # Map of attribute id to value
        self.attributes: Dict[str, Attribute] = {}

    def json(self):
        """ Get the json returned in the object definition """
        return [x.json() for x in self.attributes.values()]

    def load(self, parent_id: str, items: list):
        """ Parse the data to create the attributes """
        if not isinstance(items, list):
            raise errors.ValidationError(f"Object '{parent_id}' attributes are invalid. Must be a list of json objects.")

        for item in items:
            attribute = Attribute.load(parent_id, item)
            self.attributes[attribute.id] = attribute

    def set(
            self,
            id: str,
            name: str = None,
            value: Union[int, float] = None,
            icon: Optional[str] = None
    ):
        """ Set an attribute when loading a tile/entity definition not in the standard attributes list """
        attr = Attribute()
        attr.id = id
        attr.name = name
        attr.default = value
        attr.icon = icon

        self.attributes[id] = attr

    def get_db_objects(self, instance: Union[UnitInstance, UnitInstance]):
        """ Extract the new db objects, this function exists to allow
        for bulk attribute insertion when generating the map.
        """
        return [
            instance.create_attribute_db_object(attribute.id, attribute.default)
            for attribute in self.attributes.values()
        ]

    def save_to_db(self, instance: Union[UnitInstance, UnitInstance], commit=True):
        """ Store the attributes in the db """
        for attribute in self.attributes.values():
            instance.set_attribute(attribute.id, attribute.default, commit=False)

        if commit:
            db.session.commit()


