from velvet_dawn.config import Config
from velvet_dawn.models.coordinate import Coordinate


__neighbour_cache = {}


def reset_cache():
    __neighbour_cache.clear()


def get_neighbours(coord: Coordinate, config: Config):
    if coord.__hash__() in __neighbour_cache:
        return __neighbour_cache[coord.__hash__()]

    is_odd = coord.x % 2 == 1
    coords = [
        Coordinate(x=coord.x - 1, y=coord.y if is_odd else coord.y - 1),
        Coordinate(x=coord.x - 1, y=coord.y + 1 if is_odd else coord.y),
        Coordinate(x=coord.x, y=coord.y - 1),
        Coordinate(x=coord.x, y=coord.y + 1),
        Coordinate(x=coord.x + 1, y=coord.y if is_odd else coord.y - 1),
        Coordinate(x=coord.x + 1, y=coord.y + 1 if is_odd else coord.y),
    ]

    oords = list(filter(lambda coord: 0 <= coord.x < config.map_width and 0 <= coord.y < config.map_height, coords))
    __neighbour_cache[coord.__hash__()] = oords

    return oords


# TODO Test
def get_neighbours_in_range(current_tile, tile_range, config: Config):
    neighbours = {current_tile}
    for _ in range(tile_range):
        new_neighbours = set()
        for oord in neighbours:
            # load all neighbours regardless of the map size as we'll filter later
            new_neighbours.update(get_neighbours(oord, config=config))
        neighbours.update(new_neighbours)
    return neighbours
