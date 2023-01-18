import velvet_dawn


""" This world instance exists to allow the user
to set attributes and tags on the world which is
not tied to a player, unit ot tile.

This can be accessed through the 'world' selector.
"""


class WorldInstance:

    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(WorldInstance, cls).__new__(cls)
        return cls.instance

    @property
    def id(self):
        return "world"

    @staticmethod
    def set_attribute(key, value):
        velvet_dawn.db.attributes.set_world_attribute(key, value)

    @staticmethod
    def get_attribute(key, default=None):
        return velvet_dawn.db.attributes.get_world_attribute(key, default=default)

    @staticmethod
    def reset_attribute(key, value_if_not_exists):
        velvet_dawn.db.attributes.reset_world_attribute(key, value_if_not_exists)

    @staticmethod
    def add_tag(tag: str):
        velvet_dawn.db.tags.add_world_tag(tag)

    @staticmethod
    def remove_tag(tag: str):
        velvet_dawn.db.tags.remove_world_tag(tag)

    @staticmethod
    def has_tag(tag: str):
        return velvet_dawn.db.tags.is_world_tagged(tag)
