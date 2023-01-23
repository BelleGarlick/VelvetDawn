import json
import os.path

import redis
from typing import Optional, List

from velvet_dawn import errors
from velvet_dawn.config import Config


# TODO Document what this is and how it works
# TODO Test running unit tests utilising redis


redis_connection: Optional[redis.Redis] = None
_data = {}


def instantiate(config: Config):
    pass


def clear():
    global _data

    if redis_connection:
        redis_connection.flushall()
    _data = {}

    save()


def set_redis():
    # TODO
    pass


def dump_data_json(data: dict):
    exported_data = {}
    for key in data:
        if isinstance(data[key], list):
            exported_data[key] = ["__list__"] + data[key]
        elif isinstance(data[key], set):
            exported_data[key] = ["__set__"] + list(data[key])
        elif isinstance(data[key], dict):
            exported_data[key] = dump_data_json(data[key])
        else:
            exported_data[key] = data[key]

    return exported_data


def parse_data_json(data: dict):
    parsed_data = {}
    for key in data:
        if isinstance(data[key], list):
            if data[key][0] == "__list__":
                parsed_data[key] = data[key][1:]
            elif data[key][0] == "__set__":
                parsed_data[key] = set(data[key][1:])
            else:
                raise errors.ValidationError("Invalid json data. All lists must start with item '__list__' or '__set__'")
        elif isinstance(data[key], dict):
            parsed_data[key] = parse_data_json(data[key])
        else:
            parsed_data[key] = data[key]

    return parsed_data


def save():
    # TODO Save into specific worlds
    with open("data.json", "w+") as file:
        file.write(json.dumps(dump_data_json(_data), indent=4))


def load():
    global _data
    if os.path.exists("data.json"):
        with open("data.json") as file:
            _data = parse_data_json(json.load(file))


def set_value(key: str, value: str):
    if redis_connection:
        redis_connection.set(key, value)
    else:
        _data[key] = value


def get_value(key, default=None):
    if redis_connection:
        return redis_connection.get(key) or default
    return _data.get(key, default)


def rem(key: str):
    if redis_connection:
        return redis_connection.delete(key, )
    elif key in _data:
        del _data[key]


"""
Set Operations
"""


def sadd(name: str, values: List[str]):
    if redis_connection:
        redis_connection.sadd(name, *values)
    else:
        if name not in _data:
            _data[name] = set()
        _data[name].update(values)


def srem(name: str, values: List[str]):
    if redis_connection:
        redis_connection.srem(name, *values)
    else:
        if name in _data and isinstance(_data[name], set):
            for value in values:
                if name in _data and value in _data[name]:
                    _data[name].remove(value)

            if not _data[name]:
                del _data[name]


def smembers(name):
    if redis_connection:
        redis_connection.smembers(name)
    else:
        if name in _data and isinstance(_data[name], set):
            return _data[name]
    return set()


def sismember(name, value):
    if redis_connection:
        return redis_connection.sismember(name, value)

    if name in _data and isinstance(_data[name], set):
        return value in _data[name]

    return False


"""
Hash Operations
"""


def hset(name, key=None, value=None):
    if redis_connection:
        redis_connection.hset(name, key=key, value=value)
    else:
        if name not in _data:
            _data[name] = {}
        _data[name][key] = value


def hget(name, key, default=None):
    if redis_connection:
        return redis_connection.hget(name, key) or default
    else:
        return _data.get(name, {}).get(key, default)


def hexists(name, key):
    if redis_connection:
        return redis_connection.hexists(name, key)
    else:
        return key in _data.get(name, {})


def hgetall(name):
    if redis_connection:
        return redis_connection.hgetall(name)
    return _data.get(name, {})


def hdel(name, key):
    if redis_connection:
        return redis_connection.hdel(name, key)
    else:
        if name in _data:
            if key in _data[name]:
                del _data[name][key]
            if not _data[name]:
                del _data[name]


def hvals(name):
    if redis_connection:
        return redis_connection.hvals(name)
    else:
        return _data.get(name, {}).values()
