import os
from typing import Dict
from pathlib import Path
from config import Config
from velvet_dawn.models.resource import Resource, ResourceType

DATA_PATH = Path("../../datapacks/")

resources: Dict[str, Resource] = {}


def initialise(config: Config):
    print("Initialising Resources")
    global resources

    if not DATA_PATH.exists():
        raise Exception("data/resources does not exist")

    resources = {}
    for datapack in config.datapacks:
        resource_path = DATA_PATH / datapack / 'resources'
        if not resource_path.exists():
            continue

        resource_files = os.listdir(resource_path)

        for file in resource_files:
            print(f" - {datapack}/{file}")
            path = Path(resource_path / file)
            resource_id = f"{datapack}/{path.stem}"

            file_type, resource_type = path.suffix[1:], ResourceType.Audio
            if file_type in {"mp3"}: resource_type = ResourceType.Audio
            elif file_type in {"jpg", "png"}: resource_type = ResourceType.Image
            else:
                raise Exception(f"Resource '{path}' is invalid. File types may only be mp3, jpg or png")

            resources[resource_id] = Resource(
                id=resource_id,
                path=path,
                resource_type=resource_type
            )


def get_resources() -> Dict[str, Resource]:
    return resources
