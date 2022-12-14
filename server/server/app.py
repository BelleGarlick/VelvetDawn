from flask import request, send_file
from functools import wraps

import errors
import velvet_dawn
from config import Config
from dao.initialisation import app


config = Config.load()


def validator():
    def decorator(fun):
        @wraps(fun)
        def wrapper(*args, **kwargs):
            password = request.form.get("password", request.args.get("password", None))
            print(password)
            # TODO Load config

            try:
                return fun(*args, **kwargs)

            except errors.ValidationError as e:
                return e, 400

            except Exception as e:
                print(e)
        return wrapper
    return decorator


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
    return velvet_dawn.map.get()


@app.route("/map/tiles/")
def get_map_tiles():
    return [
        tile.json()
        for tile in
        velvet_dawn.map.tiles.get_tiles().values()
    ]


@app.route("/resources/")
def get_resources():
    return [
        resource.json()
        for resource in
        velvet_dawn.resources.get_resources().values()
    ]


@app.route("/resources/<resource_id>/")
def get_resource(resource_id):
    resource = velvet_dawn.resources.get_resources().get(resource_id)
    if not resource:
        return "File not found", 404
    return send_file(resource.path)


@app.route("/entities/")
def get_entities():
    return [
        entity.json()
        for entity in
        velvet_dawn.entities.get_entities().values()
    ]


@app.route("/entities/setup/")
def get_entity_setup():
    return velvet_dawn.game.initial_entities()


@app.route("/game-state/")
def get_game_state():
    return {
        "phase": velvet_dawn.game.phase(),
        "turn": velvet_dawn.game.turn(),
        "activeTurn": velvet_dawn.game.active_turn(),
        "teams": [
            team.json()
            for team in velvet_dawn.teams.list()
        ]
    }


@app.route("/join/", methods=["POST"])
def join_game():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username and not password:
        return "Missing keys in request", 400

    return velvet_dawn.players.join(username, password).json()


if __name__ == "__main__":
    velvet_dawn.entities.initialise(config)
    velvet_dawn.map.tiles.initialise(config)
    velvet_dawn.resources.initialise(config)

    with app.app_context():
        velvet_dawn.map.new(20, 10)

    velvet_dawn.entities.get_entities()

    app.run("0.0.0.0", port=config.port, debug=True)
