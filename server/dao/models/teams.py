from sqlalchemy.orm import relationship

from dao.initialisation import db


class Team(db.Model):
    __tablename__ = 'teams'

    name = db.Column(db.Text, primary_key=True)
    color = db.Column(db.Text)

    team_members = relationship("Player")

    def json(self):
        return {
            "name": self.name,
            "color": self.color,
            "players": [
                player.json() for player in self.team_members
            ]
        }
