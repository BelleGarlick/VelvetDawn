from velvet_dawn.dao import db


class UnitAttribute(db.Model):
    __tablename__ = 'unit_attributes'

    instance_id = db.Column(db.Integer, primary_key=True)

    key = db.Column(db.String, nullable=False, primary_key=True)
    value = db.Column(db.String)

    update_time = db.Column(db.Integer, nullable=False)

    def json(self):
        return {
            "instanceId": self.instance_id,
            "key": self.key,
            "value": self.value
        }


class TileAttribute(db.Model):
    __tablename__ = 'tile_attributes'

    instance_id = db.Column(db.Integer, primary_key=True)

    key = db.Column(db.String, nullable=False, primary_key=True)
    value = db.Column(db.String)

    update_time = db.Column(db.Integer, nullable=False)

    def json(self):
        return {
            "instanceId": self.instance_id,
            "key": self.key,
            "value": self.value
        }
