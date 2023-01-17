from sqlalchemy.orm import relationship

import velvet_dawn
from velvet_dawn.dao import db


class TileInstance(db.Model):

    __tablename__ = 'tiles'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    tile_id = db.Column(db.Integer, nullable=False)

    # Grid position
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)

    db.UniqueConstraint(x, y)

    def set_attribute(self, key, value):
        velvet_dawn.dao.attributes.set_tile_attribute(self.id, key, value)

    def get_attribute(self, key, default=None):
        return velvet_dawn.dao.attributes.get_tile_attribute(self.id, key, default=default)

    def reset_attribute(self, key, value_if_not_exists):
        velvet_dawn.dao.attributes.reset_tile_attribute(self.id, key, value_if_not_exists)

    def add_tag(self, tag: str):
        velvet_dawn.dao.tags.add_tile_tag(self.id, tag)

    def remove_tag(self, tag: str):
        velvet_dawn.dao.tags.remove_tile_tag(self.id, tag)

    def has_tag(self, tag: str):
        return velvet_dawn.dao.tags.is_tile_tagged(self.id, tag)

    def json(self):
        return {
            "id": self.id,
            "tileId": self.tile_id,
            "position": {
                "x": self.x,
                "y": self.y
            }
        }
