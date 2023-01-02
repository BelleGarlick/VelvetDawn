import time

import velvet_dawn.dao
from velvet_dawn.dao import db
from velvet_dawn.dao.models.attributes import UnitAttribute
from velvet_dawn.dao.models.players import Player


class UnitInstance(db.Model):
    __tablename__ = 'units'

    id = db.Column(db.Integer, primary_key=True)

    player = db.Column(db.Text, db.ForeignKey(Player.name), nullable=False)

    entity_id = db.Column(db.Text, nullable=False)

    # Grid position
    x = db.Column(db.Integer, nullable=False)
    y = db.Column(db.Integer, nullable=False)

    @property
    def pos_x(self):
        return self.x

    @property
    def pos_y(self):
        return self.y

    def get_attribute(self, key: str, _type=None, default=None):
        value = db.session.query(UnitAttribute)\
            .where(
                UnitAttribute.instance_id == self.id,
                UnitAttribute.key == key
            ).one_or_none()

        if value:
            return velvet_dawn.utils.parse_type(value.value, _type, default)

        return default

    def create_attribute_db_object(self, key, value):
        attr = UnitAttribute(
            instance_id=self.id,
            key=key,
            update_time=int(time.time())
        )
        if value is not None:
            attr.value = str(value)
        return attr

    def set_attribute(self, key: str, value, commit=True):
        db.session.query(UnitAttribute)\
            .where(
                UnitAttribute.instance_id == self.id,
                UnitAttribute.key == key
            ).delete()

        db.session.add(self.create_attribute_db_object(key, value))

        if commit:
            db.session.commit()

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
