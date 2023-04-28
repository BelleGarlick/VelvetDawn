import velvet_dawn
from velvet_dawn.db.instances.instance import Instance

""" This world instance exists to allow the user
to set attributes and tags on the world which is
not tied to a player, unit ot tile.

This can be accessed through the 'world' selector.
"""


class OldWorldInstance(Instance):

    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(OldWorldInstance, cls).__new__(cls)
        return cls.instance

    @property
    def id(self):
        return "world"

    @property
    def entity_id(self):
        return "world"

    def __hash__(self):
        return hash("world")

    def set_attribute(self, key, value):
        velvet_dawn.db.attributes.set_world_attribute(key, value)

    def get_attribute(self, key, default=None):
        return velvet_dawn.db.attributes.get_world_attribute(key, default=default)

    def reset_attribute(self, key, value_if_not_exists):
        velvet_dawn.db.attributes.reset_world_attribute(key, value_if_not_exists)

