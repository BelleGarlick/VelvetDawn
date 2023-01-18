import velvet_dawn.db.tags
from velvet_dawn.dao import db
from velvet_dawn.dao.models.players import Player


class UnitInstance(db.Model):
    __tablename__ = 'units'

    id = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.Text, nullable=False)

    commander = db.Column(db.Boolean, nullable=False)

    player = db.Column(db.Text, db.ForeignKey(Player.name), nullable=False)

    # Grid position
    x = db.Column(db.Integer, nullable=False)
    y = db.Column(db.Integer, nullable=False)

    def set_attribute(self, key, value):
        velvet_dawn.db.attributes.set_unit_attribute(self.id, key, value)

    def get_attribute(self, key, default=None):
        return velvet_dawn.db.attributes.get_unit_attribute(self.id, key, default=default)

    def reset_attribute(self, key, value_if_not_exists):
        velvet_dawn.db.attributes.reset_unit_attribute(self.id, key, value_if_not_exists)

    def add_tag(self, tag: str):
        velvet_dawn.db.tags.add_unit_tag(self.id, tag)

    def remove_tag(self, tag: str):
        velvet_dawn.db.tags.remove_unit_tag(self.id, tag)

    def has_tag(self, tag: str):
        return velvet_dawn.db.tags.is_unit_tagged(self.id, tag)

    def json(self):
        return {
            "id": self.id,
            "player": self.player,
            "entity": self.entity_id,
            "position": {
                "x": self.x,
                "y": self.y
            }
        }
