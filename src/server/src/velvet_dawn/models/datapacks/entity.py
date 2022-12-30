import dataclasses
from .custom_attributes import CustomAttributes
from velvet_dawn.models.datapacks.taggable import Taggable


@dataclasses.dataclass
class EntityCombat:
    damage = 0
    range = 1
    radius = 1

    def update(self, data: dict):
        self.damage = data.get('damage', self.damage)
        self.range = data.get('range', self.range)
        self.radius = data.get('radius', self.radius)

    def json(self):
        return {
            "damage": self.damage,
            "range": self.range,
            "radius": self.radius
        }


# TODO add proper class and tests like tile movement

@dataclasses.dataclass
class EntityMovement:
    range = 2

    def update(self, data: dict):
        self.range = data.get('range', self.range)

    def json(self):
        return {
            "range": self.range
        }


# TODO Standard
# TODO Moving
# TODO Fighting
# TODO Movement particles
class EntityTextures:
    def __init__(self):
        self.background = None

    def update(self, data: dict):
        self.background = data.get("background")

    def json(self):
        return {
            "background": self.background
        }


class Entity(Taggable):
    def __init__(self, id: str, name: str):
        super().__init__()

        self.id = id
        self.name = name
        self.max_health = 100
        self.commander = False

        self.attributes = CustomAttributes()
        self.combat = EntityCombat()
        self.movement = EntityMovement()
        self.textures = EntityTextures()

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "commander": self.commander,
            "health": {
                "max": self.max_health
            },
            "attributes": self.attributes.json(),
            "movement": self.movement.json(),
            "combat": self.combat.json(),
            "textures": self.textures.json()
        }

    @staticmethod
    def load(id: str, data: dict):
        entity = Entity(id=id, name=data['name'])

        entity.commander = data.get("commander", False)
        entity.combat.update(data.get('combat', {}))
        entity.movement.update(data.get('movement', {}))
        entity.textures.update(data.get('textures', {}))
        entity.attributes = CustomAttributes.load(id, data.get('attributes', []))

        entity._load_tags(data)

        return entity
