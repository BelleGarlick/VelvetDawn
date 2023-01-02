from velvet_dawn.dao import db


class SpawnArea(db.Model):
    __tablename__ = 'spawn_area'

    team = db.Column(db.Text, primary_key=True, nullable=False)
    x = db.Column(db.Integer, primary_key=True, nullable=False)
    y = db.Column(db.Integer, primary_key=True, nullable=False)

    def json(self):
        return {
            "team": self.team,
            "x": self.x,
            "y": self.y
        }