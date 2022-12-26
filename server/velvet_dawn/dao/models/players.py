from constants import SPECTATORS_TEAM_ID
from velvet_dawn.dao import db


class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.Text)
    password = db.Column(db.Text)  # passcode when loging in

    team = db.Column(db.Text)

    admin = db.Column(db.Boolean, default=False)

    ready = db.Column(db.Boolean, default=False)

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "team": self.team,
            "admin": self.admin,
            "ready": self.ready,
            "spectating": self.team == SPECTATORS_TEAM_ID
        }
