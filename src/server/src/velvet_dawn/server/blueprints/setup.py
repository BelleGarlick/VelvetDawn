import velvet_dawn
from flask import Blueprint, request

from velvet_dawn.dao.models import Player
from velvet_dawn.models.phase import Phase
from velvet_dawn.server.utils import api_wrapper, config

setup_blueprint = Blueprint('setup_blueprint', __name__)


@setup_blueprint.route("/", methods=["POST"])
@api_wrapper(host_only=True)
def update_game_setup(user):
    entity_id = request.form.get("entity")
    count = int(request.form.get("count"))

    velvet_dawn.game.setup.update_setup(entity_id, count)

    return velvet_dawn.game.setup.get_setup(user.name).json()


@setup_blueprint.route("/add/", methods=["POST"])
@api_wrapper(return_state=True)
def add_entity_during_setup(user):
    entity = request.form.get("entity")
    x = int(request.form.get("x"))
    y = int(request.form.get("y"))

    velvet_dawn.game.setup.place_entity(user.name, entity, x, y, config)


@setup_blueprint.route("/remove/", methods=["POST"])
@api_wrapper(return_state=True)
def remove_entity_during_setup(user: Player):
    x = int(request.form.get("x"))
    y = int(request.form.get("y"))

    velvet_dawn.game.setup.remove_entity(user.name, x, y)


@setup_blueprint.route("/start-setup/", methods=["POST"])
@api_wrapper(return_state=True, host_only=True)
def start_game_setup(user):
    if velvet_dawn.game.phase.get_phase() == Phase.Lobby:
        velvet_dawn.game.phase.start_setup_phase(config)