from sqlalchemy.orm import relationship

from velvet_dawn.dao import db
from velvet_dawn.dao.models.players import Player


class UnitInstance(db.Model):
    __tablename__ = 'units'

    id = db.Column(db.Integer, primary_key=True)

    player = db.Column(db.Text, db.ForeignKey(Player.name), nullable=False)

    entity_id = db.Column(db.Text, nullable=False)

    # Grid position
    x = db.Column(db.Integer, nullable=False)
    y = db.Column(db.Integer, nullable=False)

    attributes = relationship("Attribute", cascade="all, delete")
    tags = relationship("Tag", cascade="all, delete")

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

    def create_db_tag_obj(self, tag):
        from velvet_dawn.dao.models.tags import TagParent, create_tag_obj
        return create_tag_obj(self.id, TagParent.Unit, tag)

    def add_tag(self, tag: str, commit=True):
        from velvet_dawn.dao.models.tags import TagParent, add_tag
        add_tag(self.id, TagParent.Unit, tag, commit=commit)

    def remove_tag(self, tag: str, commit=True):
        from velvet_dawn.dao.models.tags import TagParent, remove_tag
        remove_tag(self.id, TagParent.Unit, tag, commit=commit)

    def has_tag(self, tag: str):
        from velvet_dawn.dao.models.tags import TagParent, has_tag
        return has_tag(self.id, TagParent.Unit, tag)

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
