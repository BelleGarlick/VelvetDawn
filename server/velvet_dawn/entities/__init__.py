import os
from typing import Dict
from pathlib import Path
from config import Config
from velvet_dawn.models.entity import Entity


ENTITY_PATH = Path(__file__).parent.parent.parent.parent / "datapacks"

entities: Dict[str, Entity] = {}


def initialise(config: Config):
    print("Initialising Entities")
    global entities

    if not ENTITY_PATH.exists():
        raise Exception("data/entities does not exist")

    entities = {}
    for datapack in config.datapacks:
        entities_path = ENTITY_PATH / datapack / 'entities'
        if not entities_path.exists():
            continue

        entity_files = os.listdir(entities_path)

        for file in entity_files:
            print(f" - {datapack}/{file}")
            entity = Entity.load(entities_path / file)
            entities[entity.id] = entity


def get_entities() -> Dict[str, Entity]:
    return entities
