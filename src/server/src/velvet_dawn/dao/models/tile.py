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

    attributes = relationship("Attribute", cascade="all, delete")

    db.UniqueConstraint(x, y)

    @property
    def entity_id(self):
        return self.tile_id

    def create_db_attribute_obj(self, key: str, value):
        from velvet_dawn.dao.models.attributes import AttributeParent, create_attribute_db_object
        return create_attribute_db_object(self.id, AttributeParent.Tile, key, value)

    def set_attribute(self, key, value, commit=True):
        from velvet_dawn.dao.models.attributes import AttributeParent, set_attribute
        return set_attribute(self.id, AttributeParent.Tile, key, value, commit=commit)

    def get_attribute(self, key, default=None):
        from velvet_dawn.dao.models.attributes import AttributeParent, get_attribute
        return get_attribute(self.id, AttributeParent.Tile, key, default=default)

    def reset_attribute(self, key, value_if_not_exists, commit=True):
        from velvet_dawn.dao.models.attributes import AttributeParent, reset_attribute
        reset_attribute(self.id, AttributeParent.Tile, key, value_if_not_exists, commit=commit)

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
