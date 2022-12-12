from sqlalchemy.orm import relationship

from dao.initialisation import db
from dao.models.teams import Team


class Player(db.Model):
    __tablename__ = 'players'

    name = db.Column(db.Text, primary_key=True)
    spectating = db.Column(db.Boolean, nullable=False, default=False)
    team = db.Column(db.Text, db.ForeignKey(Team.name))

    entities = relationship("Entity", cascade="all, delete")

    def json(self):
        return {
            "name": self.name,
            "spectating": self.spectating,
            "entities": [
                entity.json() for entity in self.entities
            ]
        }
