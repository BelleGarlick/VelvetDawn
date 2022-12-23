import math
from typing import List

import errors
import velvet_dawn.map.neighbours
from config import Config
from constants import SPECTATORS_TEAM_ID
from logger import logger
from velvet_dawn.dao import db
from velvet_dawn.dao.models import Team, Player, SpawnArea
from velvet_dawn.models.coordinate import Coordinate


""" Spawn

This module handles assigning spawnable tiles for players 
at the start of the game.

When moving from the lobby to the setup phase, the allocate
spawn points should be called to setup the the team's spawn
areas
"""


def allocate_spawn_points(config: Config):
    logger.info("Allocating spawn area.")

    teams: List[Team] = db.session.query(Team).where(Team.team_id != SPECTATORS_TEAM_ID).all()
    if not teams:
        raise errors.ValidationError("No teams to allocate spawn points for")

    db.session.query(SpawnArea).delete()
    db.session.commit()

    # Count players per team to number of players per team
    max_team_size = max([
        len(db.session.query(Player).where(Player.team == team.team_id).all())
        for team in teams
    ])

    # Calculate initial spawn points
    spawn_points = _get_central_spawn_ordinates(
        config,
        team_count=len(teams),
        max_team_size=max_team_size
    )

    base_neighbours = _calculate_spawn_base_half_width(config, max_team_size)
    for i, spawn_point in enumerate(spawn_points):
        spawn_area = {spawn_point}

        initial_point = spawn_point
        for _ in range(base_neighbours):
            initial_point = _get_next_coordinate(initial_point, config)
            spawn_area.add(initial_point)

        initial_point = spawn_point
        for _ in range(base_neighbours):
            initial_point = _get_next_coordinate(initial_point, config, clockwise=False)
            spawn_area.add(initial_point)

        for _ in range(_calculate_neighbour_depth(config, max_team_size)):
            for point in list(spawn_area):
                spawn_area.update(velvet_dawn.map.neighbours.get_neighbours(point, config))

        for p in spawn_area:
            db.session.add(SpawnArea(
                team=teams[i].team_id,
                pos_x=p.x,
                pos_y=p.y,
            ))
        db.session.commit()


def get_allocated_spawn_area(user: str) -> List[SpawnArea]:
    """ Get the alocated spawn tiles for a given user """
    team = velvet_dawn.teams.get_team_for_player(user)
    if not team:
        return []

    return db.session.query(SpawnArea) \
        .where(SpawnArea.team == team.team_id) \
        .all()


def is_point_spawnable(user: str, x: int, y: int):
    """ Check if the given point exists within the player's spawn territory """
    team = velvet_dawn.teams.get_team_for_player(user)
    item = db.session.query(SpawnArea) \
        .where(SpawnArea.team == team.team_id, SpawnArea.pos_y == y, SpawnArea.pos_x == x) \
        .one_or_none()

    return bool(item)


def _calculate_spawn_base_half_width(config: Config, max_team_size: int) -> int:
    """ Calculate the number of initial sidewards neighbours before adding neighbour depth """
    return config.spawning.width_multiplier * max_team_size + config.spawning.width_addition


def _calculate_neighbour_depth(config: Config, max_team_size: int) -> int:
    """ Calculate the number of neighbouring cell depth needed """
    return config.spawning.neighbours_multiplier * max_team_size


def _calculate_spawn_area_half_width(config: Config, max_team_size: int) -> int:
    """ Calculate the half_width of the spawn areas defined by the config

    Args:
        config: Used to get spawning params
        max_team_size: Used to calculate the same spawn area size

    Returns:
        half widh
    """
    width_either_side = _calculate_spawn_base_half_width(config, max_team_size)
    width_either_side += _calculate_neighbour_depth(config, max_team_size)

    return width_either_side


def _get_central_spawn_ordinates(config: Config, team_count: int, max_team_size: int) -> List[Coordinate]:
    """ Calculate the central spawn ordinates of a spawn region for each team

    Args:
        config: For accessing spawn constraints and map sizing
        team_count: The number of teams to spawn
        max_team_size: The largest size of a teeam

    Returns:
        List of co-ordinates that define the center of the spawn area
    """
    # Calculate non-spawnable width near the corners
    inset_padding = _calculate_spawn_area_half_width(config, max_team_size)

    # Calc the number of perimeter cells that we cant to
    # distribute teams around
    map_perimeter = 2 * (config.map_width + config.map_height) - 4

    # Spacing between team cells
    corners_removed = 4 if inset_padding > 0 else 0  # If 0 width then corner spawning is possible
    spawnable_perimeter_positions = map_perimeter - (
            (2 * min(config.map_width, 2 * inset_padding))
            + (2 * min(config.map_height, 2 * inset_padding))
            - corners_removed
    )
    if spawnable_perimeter_positions <= 0:
        raise Exception("Map too small for spawning constraints. Consider increasing the map size.")
    gap_between_teams = spawnable_perimeter_positions / team_count

    # The first teams spawn point and the current team
    # cell. Every time the current_team_point rounded up
    # equals the cell we're iteraing through, we mark this
    # cell as a spawn point and increase the new team mark
    current_point = Coordinate(config.map_width // 2, 0)
    current_team_mark = 0

    spawn_points: List[Coordinate] = []
    perimeter_count = 0
    for i in range(config.map_width // 2, map_perimeter + config.map_width // 2):
        cell = _get_cell_from_perimeter_index(i % map_perimeter, config)
        if (
                inset_padding <= cell.x < config.map_width - inset_padding
                or inset_padding <= cell.y < config.map_height - inset_padding
        ):
            if math.floor(current_team_mark) == perimeter_count:
                spawn_points.append(current_point)
                current_team_mark += gap_between_teams
            perimeter_count += 1

            current_point = _get_next_coordinate(cell, config)

    return spawn_points


def _get_cell_from_perimeter_index(perimeter_index: int, config: Config) -> Coordinate:
    """ This function treats the perimeter as a band around the map
     where each item is indexable starting in the top left at index 0

    Args:
        perimeter_index: The perimeter cell to get given the index
        config: For accessing the map size

    Returns:
        Coordinate for that index
    """
    map_width, map_height = config.map_width, config.map_height

    if perimeter_index < map_width:
        return Coordinate(perimeter_index, 0)
    elif perimeter_index < map_width + map_height - 1:
        return Coordinate(map_width - 1, perimeter_index - (map_width - 1))
    elif perimeter_index < map_width + map_height + map_width - 2:
        return Coordinate(map_width - 1 - (perimeter_index - (map_height + map_width - 2)), map_height - 1)
    else:
        return Coordinate(0, map_height - 1 - (perimeter_index - (map_height + map_width + map_width - 3)))


def _get_next_coordinate(current_point: Coordinate, config: Config, clockwise=True) -> Coordinate:
    """ This function will return the next point as we walk
    around the perimeter of the map.

    This function works by treating the perimeter as a band
    that the func walks along. So, first we convert the cell
    to the perimeter, then move along the perimeter then
    back to a cell.

    Args:
        current_point: Current point to get the next point for
        config: Velvet dawn config
        clockwise: If true, the next ordinate will be clockwise else counterclockwise

    Returns:
        next ordinate
    """
    map_width, map_height = config.map_width, config.map_height

    perimeter_index = -1

    # Convert cell to perimeter index
    if current_point.y == 0: perimeter_index = current_point.x
    elif current_point.x == map_width - 1: perimeter_index = current_point.y + map_width - 1
    elif current_point.y == map_height - 1:
        perimeter_index = (map_width + map_height - 2) + (map_width - current_point.x - 1)
    elif current_point.x == 0:
        perimeter_index = (map_width + map_height + map_width - 3) + (map_height - current_point.y - 1)

    # Shift perimeter index
    if clockwise: perimeter_index += 1
    else: perimeter_index -= 1
    total_perimeter_size = 2 * (map_width + map_height) - 4
    perimeter_index = (perimeter_index + total_perimeter_size) % total_perimeter_size

    # Convert perimeter index back to cell
    return _get_cell_from_perimeter_index(perimeter_index, config)
