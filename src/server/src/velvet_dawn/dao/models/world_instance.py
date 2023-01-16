

""" This world instance exists to allow the user
to set attributes and tags on the world which is
not tied to a player, unit ot tile.

This can be accessed through the 'world' selector.
"""
import velvet_dawn.dao.tags


class WorldInstance:

    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(WorldInstance, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def create_db_attribute_obj(key: str, value):
        from velvet_dawn.dao.models.attributes import AttributeParent, create_attribute_db_object
        return create_attribute_db_object(-1, AttributeParent.World, key, value)  # No id given since world is singleton

    @staticmethod
    def set_attribute(key, value, commit=True):
        from velvet_dawn.dao.models.attributes import AttributeParent, set_attribute
        return set_attribute(-1, AttributeParent.World, key, value, commit=commit)

    @staticmethod
    def get_attribute(key, default=None):
        from velvet_dawn.dao.models.attributes import AttributeParent, get_attribute
        return get_attribute(-1, AttributeParent.World, key, default=default)

    @staticmethod
    def reset_attribute(key, value_if_not_exists):
        from velvet_dawn.dao.models.attributes import AttributeParent, reset_attribute
        reset_attribute(-1, AttributeParent.World, key, value_if_not_exists)

    @staticmethod
    def add_tag(tag: str):
        velvet_dawn.dao.tags.add_world_tag(tag)

    @staticmethod
    def remove_tag(tag: str):
        velvet_dawn.dao.tags.remove_world_tag(tag)

    @staticmethod
    def has_tag(tag: str):
        return velvet_dawn.dao.tags.is_world_tagged(tag)
