from dao.initialisation import db


class EntitySetup(db.Model):
    __tablename__ = 'entity_setup'

    entity_id = db.Column(db.Text, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)

    def json(self):
        return {
            "id": self.entity_id,
            "amount": self.amount
        }
