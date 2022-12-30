from velvet_dawn.dao import db
from velvet_dawn.dao.models.players import Player


class Entity(db.Model):
    __tablename__ = 'entities'

    id = db.Column(db.Integer, primary_key=True)

    player = db.Column(db.Text, db.ForeignKey(Player.name), nullable=False)

    entity_id = db.Column(db.Text, nullable=False)

    # Grid position
    pos_x = db.Column(db.Integer, nullable=False)
    pos_y = db.Column(db.Integer, nullable=False)

    attributes = db.Column(db.JSON, nullable=False)

    # Each turn the remaining movement will be set to the movement range which can be modified by other entities
    movement_remaining = db.Column(db.Integer, nullable=False)
    movement_range = db.Column(db.Integer, nullable=False)

    def json(self):
        return {
            "id": self.id,
            "player": self.player,
            "entity": self.entity_id,
            "position": {
                "x": self.pos_x,
                "y": self.pos_y
            },
            "movement": {
                "remaining": self.movement_remaining,
                "range": self.movement_range
            },
            "attributes": self.attributes
        }