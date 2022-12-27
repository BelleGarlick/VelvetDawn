import velvet_dawn
from flask import Blueprint

from velvet_dawn.server.utils import api_wrapper

turn_blueprint = Blueprint('turn_blueprint', __name__)


@turn_blueprint.route("/ready/", methods=["POST"])
@api_wrapper(return_state=True)
def set_player_ready(user):
    velvet_dawn.game.turns.ready(user.name)


@turn_blueprint.route("/unready/", methods=["POST"])
@api_wrapper(return_state=True)
def set_player_not_ready(user):
    velvet_dawn.game.turns.unready(user.name)
