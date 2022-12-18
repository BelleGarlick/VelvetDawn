import velvet_dawn
from flask import Blueprint, request

from velvet_dawn.models.phase import Phase

setup_blueprint = Blueprint('setup_blueprint', __name__)


@setup_blueprint.route("/")
def get_game_setup():
    return velvet_dawn.game.setup.get_setup().json()


@setup_blueprint.route("/", methods=["POST"])
def update_game_setup():
    # TODO verify admin
    entity_id = request.form.get("entity")
    count = int(request.form.get("count"))

    velvet_dawn.game.setup.update_setup(entity_id, count)

    return velvet_dawn.game.setup.get_setup().json()


@setup_blueprint.route("/add/", methods=["POST"])
def add_entity_during_setup():
    # TODO verify player
    player = request.form.get("username")
    entity = request.form.get("entity")
    x = int(request.form.get("x"))
    y = int(request.form.get("y"))

    velvet_dawn.game.setup.place_entity(player, entity, x, y)

    return velvet_dawn.game.get_state().json()


@setup_blueprint.route("/remove/", methods=["POST"])
def remove_entity_during_setup():
    # TODO verify player
    player = request.form.get("username")
    x = int(request.form.get("x"))
    y = int(request.form.get("y"))

    velvet_dawn.game.setup.remove_entity(player, x, y)

    return velvet_dawn.game.get_state().json()


@setup_blueprint.route("/start-setup/", methods=["POST"])
def start_game_setup():
    # TODO verify player is admin
    player = request.args.get("username")

    if velvet_dawn.game.phase() == Phase.Lobby:
        velvet_dawn.game.phase(Phase.Setup)

    return velvet_dawn.game.get_state().json()