import math
import random
from typing import List, Dict, Set

from dao.initialisation import db
from dao.models import KeyValues, Keys, Tile as DbTile
from velvet_dawn.models.coordinate import Coordinate
from velvet_dawn.map.tiles import get_tiles


class Map:
    __neighbour_cache: Dict[int, List[Coordinate]] = {}

    @staticmethod
    def get_neighbouring_cell_coordinates(coord: Coordinate, map_width, map_height):
        if coord.__hash__() in Map.__neighbour_cache:
            return Map.__neighbour_cache[coord.__hash__()]

        is_odd = coord.x % 2 == 1
        coords = [
            Coordinate(x=coord.x - 1, y=coord.y if is_odd else coord.y - 1),
            Coordinate(x=coord.x - 1, y=coord.y + 1 if is_odd else coord.y),
            Coordinate(x=coord.x, y=coord.y - 1),
            Coordinate(x=coord.x, y=coord.y + 1),
            Coordinate(x=coord.x + 1, y=coord.y if is_odd else coord.y - 1),
            Coordinate(x=coord.x + 1, y=coord.y + 1 if is_odd else coord.y),
        ]

        oords = [
            coord for coord in coords
            if 0 <= coord.x < map_width and 0 <= coord.y < map_height
        ]
        Map.__neighbour_cache[coord.__hash__()] = oords

        return oords


# TODO Optimisations
# - If cell has already been collapsed then we can don't need to check all it's neighbours
# - If cell has all tile then not much need to change it

# TODO Comment everything to then try and optimise it


def new(cols: int, rows: int):
    print("Generating Map")

    Map.cache = {}

    seed = random.randint(10000, 99999)
    random.seed(seed)

    tiles = get_tiles().values()

    # TODO This should be strings in a set not list
    map: List[List[Set[str]]] = [
        [{tile.id for tile in tiles} for _ in range(rows)]
        for _ in range(cols)
    ]
    unchecked_cells = set()
    for x in range(cols):
        for y in range(rows):
            unchecked_cells.add(Coordinate(x, y))

    next_cell = get_next_tile(unchecked_cells)
    i = 0
    while next_cell:
        print(f"\r{i + 1}/{cols*rows}", end="")
        i += 1
        collapse_cell(map, next_cell, cols, rows)
        next_cell = get_next_tile(unchecked_cells)
    print("\rCompleted.")

    db.session.query(DbTile).delete()

    for col in range(len(map)):
        for row in range(len(map[0])):
            item = map[col][row].pop()
            db.session.add(DbTile(x=col, y=row, tile_id=item))
            print(item[10] + " ", end="")
        print()

    db.session.merge(KeyValues(key=Keys.MAP_WIDTH, value=str(cols)))
    db.session.merge(KeyValues(key=Keys.MAP_HEIGHT, value=str(rows)))
    db.session.commit()


def get_next_tile(unchecked_cells: Set[Coordinate]):
    if not unchecked_cells:
        return None

    cell = random.choice(list(unchecked_cells))
    unchecked_cells.remove(cell)
    return cell


def get_possible_neighbours(cell_options: Set[str], tile_map: dict):
    possible_tiles = set()
    for option in cell_options:
        possible_tiles.update(list(tile_map[option].neighbours))
    return possible_tiles


def collapse_cell(map: List[List[Set[str]]], cell: Coordinate, map_width, map_height):
    tile_map = get_tiles()

    # TODO Only get probabilities from fully collapsed cells
    callapsed_cell_probs = []
    cell_probabilites = get_neighbouring_cell_probabilities(map, cell, map_width, map_height)
    for key in cell_probabilites:
        callapsed_cell_probs += [key] * cell_probabilites[key]

    cell_choise = random.choice(callapsed_cell_probs)
    map[cell.x][cell.y] = {cell_choise}
    possible_neighbours = get_possible_neighbours(map[cell.x][cell.y], tile_map)

    neighbour_updates = [
        (possible_neighbours, Map.get_neighbouring_cell_coordinates(coord=cell, map_width=map_width, map_height=map_height))
    ]

    total_cell_updagtes = 0
    while neighbour_updates:
        total_cell_updagtes += 1
        possible_neighbours, cells = neighbour_updates.pop()
        for neighbour in cells:
            current_possibilities = len(map[neighbour.x][neighbour.y])
            map[neighbour.x][neighbour.y] = map[neighbour.x][neighbour.y].intersection(possible_neighbours)
            if len(map[neighbour.x][neighbour.y]) < current_possibilities:
                neighbour_updates.append((
                    get_possible_neighbours(map[neighbour.x][neighbour.y], tile_map),
                    Map.get_neighbouring_cell_coordinates(coord=neighbour, map_width=map_width, map_height=map_height)
                ))

    # print()
    # for r in range(len(map[0])):
    #     for c in range(len(map)):
    #         print(str(len(map[c][r])) + " ", end="")
    #     print()
    #
    # breakpoint()


def get_neighbouring_cell_probabilities(map: List[List[Set[str]]], cell: Coordinate, map_width, map_height) -> Dict[str, int]:
    tiles = get_tiles()

    probability_map = {tile: 0 for tile in map[cell.x][cell.y]}
    neighbouring_cell_coords = Map.get_neighbouring_cell_coordinates(cell, map_width, map_height)

    for coord in neighbouring_cell_coords:
        possible_tiles = map[coord.x][coord.y]
        if len(possible_tiles) > 1:
            continue

        possible_neighbours = {}
        for tile in possible_tiles:
            for key in tiles[tile].neighbours:
                if key not in possible_neighbours:
                    possible_neighbours[key] = 0
                possible_neighbours[key] += tiles[tile].neighbours[key]

        for key in list(probability_map):
            if key not in possible_neighbours:
                del probability_map[key]
            else:
                probability_map[key] += possible_neighbours[key]

    if sum(probability_map.values()) == 0:
        return {x: 1 for x in probability_map}

    return probability_map
