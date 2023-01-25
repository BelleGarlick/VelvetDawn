from flask import Blueprint, request

import velvet_dawn
from velvet_dawn.config import Config
from velvet_dawn.models.coordinate import Coordinate
from velvet_dawn.server.utils import api_wrapper

combat_blueprint = Blueprint('combat_blueprint', __name__)


config = Config().load()


@combat_blueprint.route("/attack", methods=["POST"])
@api_wrapper(return_state=True)
def attack_an_entity(user):
    attacker_id = request.form.get("attackerId")
    position = Coordinate(
        int(request.form.get("targetX")),
        int(request.form.get("targetY"))
    )

    velvet_dawn.units.combat.attack_entity(user, attacker_id, position)
