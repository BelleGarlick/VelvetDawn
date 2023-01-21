from velvet_dawn.dao import db


class UnitUpgrade(db.Model):
    __tablename__ = 'unit_upgrades'

    instance_id = db.Column(db.Integer, primary_key=True)
    upgrade_id = db.Column(db.String, nullable=False, primary_key=True)
