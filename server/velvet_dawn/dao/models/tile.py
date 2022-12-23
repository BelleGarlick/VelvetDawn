from velvet_dawn.dao import db


class Tile(db.Model):
    __tablename__ = 'tiles'

    tile_id = db.Column(db.Integer, nullable=False)

    # Grid position
    x = db.Column(db.Integer, primary_key=True)
    y = db.Column(db.Integer, primary_key=True)

    def json(self):
        return {
            "id": self.x * 10000 + self.y,
            "tileId": self.tile_id,
            "x": self.x,
            "y": self.y
        }
