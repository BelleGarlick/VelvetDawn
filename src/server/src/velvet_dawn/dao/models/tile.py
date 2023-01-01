import time

import velvet_dawn
from velvet_dawn.dao import db
from velvet_dawn.dao.models.attributes import TileAttribute


class TileInstance(db.Model):

    __tablename__ = 'tiles'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    tile_id = db.Column(db.Integer, nullable=False)

    # Grid position
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)

    db.UniqueConstraint(x, y)

    def get_attribute(self, key: str, _type=None, default=None):
        value = db.session.query(TileAttribute) \
            .where(
                TileAttribute.instance_id == self.id,
                TileAttribute.key == key
            ).one_or_none()

        if value:
            return velvet_dawn.utils.parse_type(value.value, _type, default)

        return default

    def create_attribute_db_object(self, key, value):
        return TileAttribute(
            instance_id=self.id,
            key=key,
            value=str(value),
            update_time=int(time.time())
        )

    def set_attribute(self, key: str, value, commit=True):
        db.session.query(TileAttribute)\
            .where(
                TileAttribute.instance_id == self.id,
                TileAttribute.key == key
            ).delete()

        db.session.add(self.create_attribute_db_object(key, value))

        if commit:
            db.session.commit()

    def json(self):
        return {
            "id": self.x * 10000 + self.y,
            "tileId": self.tile_id,
            "position": {
                "x": self.x,
                "y": self.y
            },
            "texture": self.texture_variant,
            "color": self.color,
            "attributes": {
                attribute.key: attribute.value
                for attribute in db.session.query(TileAttribute).where(
                    TileAttribute.instance_id == self.id
                ).all()
            }
        }


Tile = TileInstance
