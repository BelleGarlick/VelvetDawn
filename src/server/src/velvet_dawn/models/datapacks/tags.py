from typing import Union

from velvet_dawn import errors
from velvet_dawn.dao import db
from velvet_dawn.dao.models import TileInstance, UnitInstance


# TODO Create add_tag / remove_tag functions in modify action


class Tags:
    def __init__(self):
        self.tags = set()

    def has(self, tag: str) -> bool:
        return tag in self.tags

    def load(self, parent_id, data: list):
        """ Parse the list of tags """
        if not isinstance(data, list):
            raise errors.ValidationError(f"Tags in {parent_id} is invalid. Must be a list of strings.")

        # Update tags in the datapack tags
        final_tags = set()
        for tag in data:
            if not isinstance(tag, str):
                raise errors.ValidationError(f"Tag '{tag}' in {parent_id} is invalid. Must be a list of strings.")

            if not tag.startswith("tag:"):
                tag = f"tag:{tag}"

            final_tags.add(tag)

        self.tags = final_tags

        return self

    def get_db_objects(self, instance: Union[UnitInstance, TileInstance]):
        """ Get the list of tag objects to save to the db, used when bulk
        inserting tags into the db when the map is generated
        """
        return [
            instance.create_db_tag_obj(tag)
            for tag in self.tags
        ]

    def save_to_db(self, instance: Union[UnitInstance, TileInstance], commit=True):
        """ Save the tags to the db, used when an entity spawns """
        for tag in self.tags:
            instance.add_tag(tag, commit=False)

        if commit:
            db.session.commit()
