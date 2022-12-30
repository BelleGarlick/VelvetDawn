from velvet_dawn.dao import db


class Team(db.Model):
    __tablename__ = 'teams'

    team_id = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text)
    color = db.Column(db.Text)

    def json(self):
        from . import Player

        return {
            "id": self.team_id,
            "name": self.name,
            "color": self.color,
            "players": [
                player.name for player in db.session.query(Player).where(
                    Player.team == self.team_id
                ).all()
            ]
        }
