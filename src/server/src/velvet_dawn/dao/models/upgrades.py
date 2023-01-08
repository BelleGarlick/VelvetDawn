from velvet_dawn.dao import db
from velvet_dawn.dao.models.entities import UnitInstance


class UnitUpgrade(db.Model):
    __tablename__ = 'unit_upgrades'

    instance_id = db.Column(db.Integer, db.ForeignKey(UnitInstance.id), primary_key=True)
    upgrade_id = db.Column(db.String, nullable=False, primary_key=True)
