from sqlalchemy.orm import relationship

from constants import SPECTATORS_TEAM_ID
from dao.initialisation import db
from dao.models.teams import Team


class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.Text)
    password = db.Column(db.Text)  # passcode when loging in

    team = db.Column(db.Text)

    admin = db.Column(db.Boolean, default=False)

    entities = relationship("Entity", cascade="all, delete")

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "team": self.team,
            "admin": self.admin,
            "spectating": self.team == SPECTATORS_TEAM_ID,
            "entities": [
                entity.json() for entity in self.entities
            ]
        }
