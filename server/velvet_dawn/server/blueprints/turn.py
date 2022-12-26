import velvet_dawn
from flask import Blueprint, request

from velvet_dawn.config import Config

turn_blueprint = Blueprint('turn_blueprint', __name__)

config = Config().load()


# TODO Api tests


@turn_blueprint.route("/ready/", methods=["POST"])
def set_player_ready():
    # TODO verify user
    player = request.form.get("username")
    password = request.form.get("password")

    velvet_dawn.game.turns.ready(player)

    return velvet_dawn.game.get_state(config, player).json()


@turn_blueprint.route("/unready/", methods=["POST"])
def set_player_not_ready():
    # TODO verify user
    player = request.form.get("username")
    password = request.form.get("password")

    velvet_dawn.game.turns.unready(player)

    return velvet_dawn.game.get_state(config, player).json()
