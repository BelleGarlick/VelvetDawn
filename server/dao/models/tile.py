from sqlalchemy.orm import relationship

from dao.initialisation import db


class Tile(db.Model):
    __tablename__ = 'tiles'

    # Grid position
    x = db.Column(db.Integer, primary_key=True)
    y = db.Column(db.Integer, primary_key=True)

    tile_id = db.Column(db.Integer, nullable=False)
