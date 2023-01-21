import math

import velvet_dawn
from velvet_dawn.db.instances.instance import Instance


class UnitInstance(Instance):

    def __init__(self, data: dict):
        self.data = data

    @property
    def instance_id(self):
        return self.data["instance_id"]

    # TODO Change this to return the unit id
    @property
    def id(self):
        return self.instance_id

    # TODO Remove this
    @property
    def entity_id(self):
        return self.data["id"]

    @property
    def x(self):
        return self.data['position']["x"]

    @property
    def tile_x(self):
        return math.floor(self.x)

    @property
    def y(self):
        return self.data['position']["y"]

    @property
    def tile_y(self):
        return math.floor(self.y)

    @property
    def player(self):
        return self.data['player']

    def json(self):
        return {
            "instanceId": self.instance_id,
            "player": self.player,
            "unit": self.entity_id,
            "position": {
                "x": self.x,
                "y": self.y
            }
        }

    def set_attribute(self, key, value):
        velvet_dawn.db.attributes.set_unit_attribute(self.instance_id, key, value)

    def get_attribute(self, key, default=None):
        return velvet_dawn.db.attributes.get_unit_attribute(self.instance_id, key, default=default)

    def reset_attribute(self, key, value_if_not_exists):
        velvet_dawn.db.attributes.reset_unit_attribute(self.instance_id, key, value_if_not_exists)

    def add_tag(self, tag: str):
        velvet_dawn.db.tags.add_unit_tag(self.instance_id, tag)

    def remove_tag(self, tag: str):
        velvet_dawn.db.tags.remove_unit_tag(self.instance_id, tag)

    def has_tag(self, tag: str):
        return velvet_dawn.db.tags.is_unit_tagged(self.instance_id, tag)
