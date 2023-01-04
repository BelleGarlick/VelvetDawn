import time

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

    attributes = relationship("TileAttribute", cascade="all, delete")

    db.UniqueConstraint(x, y)

    def get_attribute(self, key: str, _type=None, default=None):
        from velvet_dawn.dao.models.attributes import TileAttribute

        value = db.session.query(TileAttribute) \
            .where(
                TileAttribute.instance_id == self.id,
                TileAttribute.key == key
            ).one_or_none()

        if value:
            return velvet_dawn.utils.parse_type(value.value, _type, default)

        return default

    def create_attribute_db_object(self, key, value):
        from velvet_dawn.dao.models.attributes import TileAttribute

        attr = TileAttribute(
            instance_id=self.id,
            key=key,
            update_time=int(time.time())
        )
        if value is not None:
            attr.value = str(value)
        return attr

    def set_attribute(self, key: str, value, commit=True):
        from velvet_dawn.dao.models.attributes import TileAttribute

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
            "id": self.id,
            "tileId": self.tile_id,
            "position": {
                "x": self.x,
                "y": self.y
            }
        }


Tile = TileInstance
