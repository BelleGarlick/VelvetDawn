from velvet_dawn.dao import db


class Tile(db.Model):
    __tablename__ = 'tiles'

    tile_id = db.Column(db.Integer, nullable=False)

    # Grid position
    x = db.Column(db.Integer, primary_key=True)
    y = db.Column(db.Integer, primary_key=True)

    texture_variant = db.Column(db.String)
    color = db.Column(db.String, nullable=False)

    def json(self):
        return {
            "id": self.x * 10000 + self.y,
            "tileId": self.tile_id,
            "x": self.x,
            "y": self.y,
            "texture": self.texture_variant,
            "color": self.color
        }
