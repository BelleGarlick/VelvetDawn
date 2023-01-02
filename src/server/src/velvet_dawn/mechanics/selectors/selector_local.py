from typing import Union, List

import velvet_dawn.map.neighbours
from velvet_dawn.dao.models import Tile, UnitInstance
from .selector import SelectorParentType, Selector
from ...config import Config

from ...models import Coordinate


""" Selector 'local-*' will all objects of the given type within the local area

Some examples:
 - {"targets": "local-units.movement.range", "add": 5}
 - {"if": "local-tiles[range=5].movement.weight", "equals": 5}
"""


class SelectorLocal(Selector):

    def __init__(self, selector_name: str = "local", parent_type: SelectorParentType = SelectorParentType.ANY):
        Selector.__init__(
            self,
            selector_name=selector_name,
            parent_type=parent_type,
            valid_filters=["id", "tag", "range", "min_range"]
        )

    def new(self):
        return SelectorLocal()

    def get_selection(self, instance: Union[Tile, UnitInstance], config: Config) -> List[Union[UnitInstance, Tile]]:
        # todo change with filter
        tile_range = 2
        current_tile = Coordinate(instance.x, instance.y)
        neighbours = velvet_dawn.map.neighbours.get_neighbours_in_range(current_tile, tile_range, config=config)

        # Load the tile instances
        instances = []
        for coord in neighbours:
            unit: UnitInstance = velvet_dawn.units.get_unit_at_position(coord.x, coord.y)
            if unit: instances.append(unit)

            tile = velvet_dawn.map.get_tile(coord.x, coord.y)
            if tile: instances.append(tile)

        return instances


class SelectorLocalUnits(Selector):
    def __init__(self, selector_name: str = "local-units", parent_type: SelectorParentType = SelectorParentType.ANY):
        Selector.__init__(
            self,
            selector_name=selector_name,
            parent_type=parent_type,
            valid_filters=["id", "tag", "range", "min_range"]
        )

    def new(self):
        return SelectorLocalUnits()

    def get_selection(self, instance: Union[Tile, UnitInstance], config: Config) -> List[Union[UnitInstance, Tile]]:
        # todo change with filter
        tile_range = 2
        current_tile = Coordinate(instance.x, instance.y)
        neighbours = velvet_dawn.map.neighbours.get_neighbours_in_range(current_tile, tile_range, config=config)

        # Load the tile instances
        units = []
        for coord in neighbours:
            unit: UnitInstance = velvet_dawn.units.get_unit_at_position(coord.x, coord.y)
            if unit:
                units.append(unit)

        return units


class SelectorLocalEnemies(Selector):
    def __init__(self):
        Selector.__init__(
            self,
            selector_name="local-enemies",
            parent_type=SelectorParentType.UNIT,
            valid_filters=["id", "tag", "range", "min_range"]
        )

    def new(self):
        return SelectorLocalEnemies()

    def get_selection(self, instance: Union[Tile, UnitInstance], config: Config) -> List[Union[UnitInstance, Tile]]:
        # todo change with filter
        tile_range = 2
        current_tile = Coordinate(instance.x, instance.y)
        neighbours = velvet_dawn.map.neighbours.get_neighbours_in_range(current_tile, tile_range, config=config)

        # Load player names on the same team
        player = velvet_dawn.players.get_player(instance.player)
        team_players = {player.name for player in velvet_dawn.players.list(team=player.team)}

        # Load the tile instances
        units = []
        for coord in neighbours:
            unit: UnitInstance = velvet_dawn.units.get_unit_at_position(coord.x, coord.y)
            if unit and unit.player not in team_players:
                units.append(unit)

        return units


class SelectorLocalFriendlies(Selector):
    def __init__(self):
        Selector.__init__(
            self,
            selector_name="local-friendlies",
            parent_type=SelectorParentType.UNIT,
            valid_filters=["id", "tag", "range", "min_range"]
        )

    def new(self):
        return SelectorLocalFriendlies()

    def get_selection(self, instance: Union[Tile, UnitInstance], config: Config) -> List[Union[UnitInstance, Tile]]:
        # todo change with filter
        tile_range = 2
        current_tile = Coordinate(instance.x, instance.y)
        neighbours = velvet_dawn.map.neighbours.get_neighbours_in_range(current_tile, tile_range, config=config)

        # Load player names on the same team
        player = velvet_dawn.players.get_player(instance.player)
        team_players = {player.name for player in velvet_dawn.players.list(team=player.team)}

        # Load the tile instances
        units = []
        for coord in neighbours:
            unit: UnitInstance = velvet_dawn.units.get_unit_at_position(coord.x, coord.y)
            if unit and unit.player in team_players:
                units.append(unit)

        return units


class SelectorLocalTiles(Selector):
    def __init__(self):
        Selector.__init__(
            self,
            selector_name="local-tiles",
            parent_type=SelectorParentType.ANY,
            valid_filters=["id", "tag", "range", "min_range"]
        )

    def new(self):
        return SelectorLocalTiles()

    def get_selection(self, instance: Union[Tile, UnitInstance], config: Config) -> List[Union[UnitInstance, Tile]]:
        # todo change with filter
        tile_range = 2
        current_tile = Coordinate(instance.x, instance.y)
        neighbours = velvet_dawn.map.neighbours.get_neighbours_in_range(current_tile, tile_range, config=config)

        # Load the tile instances
        tiles = []
        for coord in neighbours:
            tile = velvet_dawn.map.get_tile(coord.x, coord.y)
            if tile:
                tiles.append(tile)

        return tiles
