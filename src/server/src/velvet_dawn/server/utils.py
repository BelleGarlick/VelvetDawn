from functools import wraps
from flask import request

import velvet_dawn.game
from velvet_dawn import errors
from velvet_dawn.config import Config
from velvet_dawn.logger import logger

config = Config.load()


def api_wrapper(return_state: bool = False, host_only: bool = False):
    def decorator(fun):
        @wraps(fun)
        def wrapper(*args, **kwargs):
            username = request.form.get("username", request.args.get("username", None))
            password = request.form.get("password", request.args.get("password", None))
            full_game_state = request.form.get("full-state", request.args.get("full-state", None))

            user = velvet_dawn.players.get_player(username)
            if not user:
                return "User does not exist", 401
            if user.password != password:
                return "Invalid authentication", 401
            if host_only and not user.admin:
                return "Host only endpoint", 401

            try:
                kwargs['user'] = user

                response = fun(*args, **kwargs)

                if return_state:
                    return velvet_dawn.game.get_state(config, username, full_state=full_game_state == "true").json()

                return response

            except errors.ValidationError as e:
                logger.error(e)
                return str(e), 400

            except Exception as e:
                logger.error(e)

        return wrapper
    return decorator
