from sqlalchemy.orm import relationship

import velvet_dawn.dao.tags
from velvet_dawn.dao import db
from velvet_dawn.dao.models.players import Player


class UnitInstance(db.Model):
    __tablename__ = 'units'

    id = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.Text, nullable=False)

    commander = db.Column(db.Boolean, nullable=False)

    player = db.Column(db.Text, db.ForeignKey(Player.name), nullable=False)

    # Grid position
    x = db.Column(db.Integer, nullable=False)
    y = db.Column(db.Integer, nullable=False)

    attributes = relationship("Attribute", cascade="all, delete")

    @property
    def pos_x(self):
        return self.x

    @property
    def pos_y(self):
        return self.y

    def create_db_attribute_obj(self, key: str, value):
        from velvet_dawn.dao.models.attributes import AttributeParent, create_attribute_db_object
        return create_attribute_db_object(self.id, AttributeParent.Unit, key, value)

    def set_attribute(self, key, value, commit=True):
        from velvet_dawn.dao.models.attributes import AttributeParent, set_attribute
        return set_attribute(self.id, AttributeParent.Unit, key, value, commit=commit)

    def get_attribute(self, key, default=None):
        from velvet_dawn.dao.models.attributes import AttributeParent, get_attribute
        return get_attribute(self.id, AttributeParent.Unit, key, default=default)

    def reset_attribute(self, key, value_if_not_exists, commit=True):
        from velvet_dawn.dao.models.attributes import AttributeParent, reset_attribute
        reset_attribute(self.id, AttributeParent.Unit, key, value_if_not_exists, commit=commit)

    def add_tag(self, tag: str):
        velvet_dawn.dao.tags.add_unit_tag(self.id, tag)

    def remove_tag(self, tag: str):
        velvet_dawn.dao.tags.remove_unit_tag(self.id, tag)

    def has_tag(self, tag: str):
        return velvet_dawn.dao.tags.is_unit_tagged(self.id, tag)

    def json(self):
        return {
            "id": self.id,
            "player": self.player,
            "entity": self.entity_id,
            "position": {
                "x": self.x,
                "y": self.y
            }
        }
