from typing import Union

from velvet_dawn import errors
from velvet_dawn.db.instances import UnitInstance
from velvet_dawn.db.instances.tile_instance import TileInstance


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

    def save_to_db(self, instance: Union[UnitInstance, TileInstance]):
        """ Save the tags to the db, used when an entity spawns """
        for tag in self.tags:
            instance.add_tag(tag)
