from flask import request

import velvet_dawn
from velvet_dawn.dao import app
from velvet_dawn.server.blueprints import (
    setup_blueprint,
    turn_blueprint,
    datapack_blueprint
)
from velvet_dawn.server.utils import api_wrapper, config

app.register_blueprint(setup_blueprint, url_prefix="/setup")
app.register_blueprint(turn_blueprint, url_prefix="/turns")
app.register_blueprint(datapack_blueprint, url_prefix="/datapacks")


@app.after_request
def add_cors_headers(response):
    if request.referrer is not None:
        response.headers.add('Access-Control-Allow-Origin', request.referrer[:-1])
    else:
        response.headers.add('Access-Control-Allow-Origin', "*")
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Headers', 'Cache-Control')
    response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
    response.headers.add('Access-Control-Allow-Headers', 'Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')

    return response


@app.route("/ping/")
def ping():
    return "pong"


@app.route("/map/")
def get_map():
    return velvet_dawn.map.get(config)


@app.route("/game-state/")
@api_wrapper(return_state=True)
def get_game_state(user):
    if user.admin:
        velvet_dawn.game.turns.check_end_turn_case(config)


@app.route("/join/", methods=["POST"])
def join_game():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username and not password:
        return "Missing keys in request", 400

    return velvet_dawn.players.join(username, password).json()


if __name__ == "__main__":
    velvet_dawn.datapacks.init(config)

    app.run("0.0.0.0", port=config.port, debug=config.debug)
