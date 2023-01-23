import math

import velvet_dawn
from velvet_dawn.db.instances.instance import Instance


class TileInstance(Instance):

    def __init__(self, tile_instance: str, tile_id: str, x: int, y: int):
        self.tile_instance = tile_instance
        self.tile_id = tile_id
        self.x = x
        self.y = y

    @property
    def instance_id(self):
        return self.tile_instance

    # TODO Change this to return the tile id
    @property
    def id(self):
        return self.instance_id

    # TODO Remove this
    @property
    def entity_id(self):
        return self.tile_id

    @property
    def tile_x(self):
        return math.floor(self.x)

    @property
    def tile_y(self):
        return math.floor(self.y)

    def __hash__(self):
        return hash(f"tile#{self.instance_id}")

    def json(self):
        return {
            "instanceId": self.instance_id,
            "tile": self.tile_id,
            "position": {
                "x": self.x,
                "y": self.y
            }
        }

    def set_attribute(self, key, value):
        velvet_dawn.db.attributes.set_tile_attribute(self.instance_id, key, value)

    def get_attribute(self, key, default=None):
        return velvet_dawn.db.attributes.get_tile_attribute(self.instance_id, key, default=default)

    def reset_attribute(self, key, value_if_not_exists):
        velvet_dawn.db.attributes.reset_tile_attribute(self.instance_id, key, value_if_not_exists)

    def add_tag(self, tag: str):
        velvet_dawn.db.tags.add_tile_tag(self.instance_id, tag)

    def remove_tag(self, tag: str):
        velvet_dawn.db.tags.remove_tile_tag(self.instance_id, tag)

    def has_tag(self, tag: str):
        return velvet_dawn.db.tags.is_tile_tagged(self.instance_id, tag)
