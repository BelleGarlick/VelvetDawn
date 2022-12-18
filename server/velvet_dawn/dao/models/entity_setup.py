from velvet_dawn.dao import db


class EntitySetup(db.Model):
    __tablename__ = 'entity_setup'

    entity_id = db.Column(db.Text, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
