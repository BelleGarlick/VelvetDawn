import velvet_dawn
from flask import Blueprint, send_file

from velvet_dawn.config import Config

datapack_blueprint = Blueprint('datapack_blueprint', __name__)

config = Config().load()


@datapack_blueprint.route("/")
def get_datapack_data():
    return {
        "tiles":[
            tile.json()
            for tile in
            velvet_dawn.datapacks.tiles.values()
        ],
        "entities": [
            entity.json()
            for entity in
            velvet_dawn.datapacks.entities.values()
        ],
        "resources": [
            resource.json()
            for resource in
            velvet_dawn.datapacks.resources.values()
        ]
    }


@datapack_blueprint.route("/<resource_id>/")
def get_resource(resource_id):
    resource = velvet_dawn.datapacks.resources.get(resource_id)
    if not resource:
        return "File not found", 404
    return send_file(resource.path)