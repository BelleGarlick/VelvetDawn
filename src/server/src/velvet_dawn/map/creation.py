import random
import velvet_dawn.map.neighbours
from typing import List, Dict, Set

from velvet_dawn.config import Config
from velvet_dawn.dao import db
from velvet_dawn import datapacks
from velvet_dawn.logger import logger
from velvet_dawn.models.coordinate import Coordinate
from velvet_dawn.dao.models import KeyValues, Keys, TileInstance


# TODO Comment everything to then try and optimise it


def new(config: Config):
    velvet_dawn.map.neighbours.reset_cache()

    seed = config.seed
    if seed is None:  # need to compare against none as seed maybe 0
        seed = random.randint(10000, 99999)
    logger.info(f"Creating map with seed: {seed}.")
    random.seed(seed)

    tiles = datapacks.tiles.values()

    map: List[List[Set[str]]] = [
        [{tile.id for tile in tiles} for _ in range(config.map_height)]
        for _ in range(config.map_width)
    ]
    unchecked_cells = []
    for x in range(config.map_width):
        for y in range(config.map_height):
            unchecked_cells.append(Coordinate(x, y))

    next_cell = get_next_tile(unchecked_cells)
    i = 0
    while next_cell:
        if i % 100 == 0:
            logger.info(f"{i + 1}/{config.map_width*config.map_height}")
        i += 1
        collapse_cell(map, next_cell, config)
        next_cell = get_next_tile(unchecked_cells)
    logger.info("Completed.")

    db.session.query(TileInstance).delete()

    # TODO Test that variants and colours are picked in test
    tile_count = 0
    tiles = []
    for col in range(len(map)):
        for row in range(len(map[0])):
            item = map[col][row].pop()
            tiles.append(TileInstance(id=tile_count, x=col, y=row, tile_id=item))
            tile_count += 1

    db.session.bulk_save_objects(tiles)
    db.session.merge(KeyValues(key=Keys.MAP_WIDTH, value=str(config.map_width)))
    db.session.merge(KeyValues(key=Keys.MAP_HEIGHT, value=str(config.map_height)))
    db.session.commit()

    # Configure all tile attributes not that the tiles have been initiated
    tile_attributes = []
    for db_tile in db.session.query(TileInstance).all():
        tile = datapacks.tiles[db_tile.tile_id]
        tile.attributes.set("texture.color", value=tile.textures.choose_color())
        tile.attributes.set("texture.background", value=tile.textures.choose_image())
        attrs = tile.attributes.get_db_objects(db_tile)
        tile_attributes += attrs
    db.session.bulk_save_objects(tile_attributes)
    db.session.commit()


def get_next_tile(unchecked_cells: List[Coordinate]):
    if not unchecked_cells:
        return None

    cell = random.choice(unchecked_cells)
    unchecked_cells.remove(cell)
    return cell


def get_possible_neighbours(cell_options: Set[str], tile_map: dict):
    possible_tiles = set()
    for option in cell_options:
        possible_tiles.update(list(tile_map[option].neighbours))

    return possible_tiles


def collapse_cell(map: List[List[Set[str]]], cell: Coordinate, config: Config):
    # TODO Only get probabilities from fully collapsed cells
    callapsed_cell_probs = []
    cell_probabilites = get_neighbouring_cell_probabilities(map, cell, config)
    for key in cell_probabilites:
        callapsed_cell_probs += [key] * cell_probabilites[key]

    cell_choice = random.choice(sorted(callapsed_cell_probs))
    map[cell.x][cell.y] = {cell_choice}
    possible_neighbours = get_possible_neighbours(map[cell.x][cell.y], datapacks.tiles)

    neighbour_updates = [
        (possible_neighbours, velvet_dawn.map.neighbours.get_neighbours(coord=cell, config=config))
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
                    get_possible_neighbours(map[neighbour.x][neighbour.y], datapacks.tiles),
                    velvet_dawn.map.neighbours.get_neighbours(coord=neighbour, config=config)
                ))

    # print()
    # for r in range(len(map[0])):
    #     for c in range(len(map)):
    #         print(str(len(map[c][r])) + " ", end="")
    #     print()
    #
    # breakpoint()


def get_neighbouring_cell_probabilities(map: List[List[Set[str]]], cell: Coordinate, config: Config) -> Dict[str, int]:
    probability_map = {tile: 0 for tile in map[cell.x][cell.y]}
    neighbouring_cell_coords = velvet_dawn.map.neighbours.get_neighbours(cell, config)

    for coord in neighbouring_cell_coords:
        possible_tiles = map[coord.x][coord.y]
        if len(possible_tiles) > 1:
            continue

        possible_neighbours = {}
        for tile in possible_tiles:
            for key in datapacks.tiles[tile].neighbours:
                if key not in possible_neighbours:
                    possible_neighbours[key] = 0
                possible_neighbours[key] += datapacks.tiles[tile].neighbours[key]

        for key in list(probability_map):
            if key not in possible_neighbours:
                del probability_map[key]
            else:
                probability_map[key] += possible_neighbours[key]

    if sum(probability_map.values()) == 0:
        return {x: 1 for x in probability_map}

    return probability_map
