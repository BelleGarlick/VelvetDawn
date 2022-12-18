from velvet_dawn.dao import db


class Tile(db.Model):
    __tablename__ = 'tiles'

    # Grid position
    x = db.Column(db.Integer, primary_key=True)
    y = db.Column(db.Integer, primary_key=True)

    tile_id = db.Column(db.Integer, nullable=False)

    def json(self):
        return {
            "id": self.tile_id,
            "x": self.x,
            "y": self.y
        }
