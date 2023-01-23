import json

import velvet_dawn
from flask import Blueprint, request

from velvet_dawn import errors
from velvet_dawn.server.utils import api_wrapper, config

units_blueprint = Blueprint('units_blueprint', __name__)


@units_blueprint.route("/move/", methods=["POST"])
@api_wrapper(return_state=True)
def move_unit(user):
    try:
        entity_pk = request.form.get("entity")
        path = json.loads(request.form.get("path"))
    except Exception:
        raise errors.ValidationError(
            f"Unable to parse id ('{request.form.get('id')}') and path ('{request.form.get('path')}')")

    velvet_dawn.units.movement.move(user, entity_pk, path, config)


@units_blueprint.route("/available-upgrades-and-abilities/")
@api_wrapper()
def get_unit_upgrade_and_abilities(user):
    instance_id = request.args.get("id")

    return {
        "abilities": velvet_dawn.units.abilities.get_unit_ability_updates(instance_id).json(),
        "upgrades": velvet_dawn.units.upgrades.get_unit_upgrade_updates(instance_id).json(),
    }


@units_blueprint.route("/upgrade/", methods=["POST"])
@api_wrapper()
def perform_unit_upgrade(user):
    instance_id = request.form.get("id")
    upgrade_id = request.form.get("upgrade")
    velvet_dawn.units.upgrades.upgrade_unit(user.name, instance_id, upgrade_id)

    return {
        "abilities": velvet_dawn.units.abilities.get_unit_ability_updates(instance_id).json(),
        "upgrades": velvet_dawn.units.upgrades.get_unit_upgrade_updates(instance_id).json(),
    }


@units_blueprint.route("/ability/", methods=["POST"])
@api_wrapper(return_state=True)
def perform_unit_ability(user):
    instance_id = request.form.get("id")
    ability_id = request.form.get("ability")
    velvet_dawn.units.abilities.run_unit_ability(user.name, instance_id, ability_id)

    return {
        "abilities": velvet_dawn.units.abilities.get_unit_ability_updates(instance_id).json(),
        "upgrades": velvet_dawn.units.upgrades.get_unit_upgrade_updates(instance_id).json(),
    }
