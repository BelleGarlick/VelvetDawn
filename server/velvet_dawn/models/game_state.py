import dataclasses
from typing import List

from velvet_dawn.dao.models import Player, Team, SpawnArea, Entity
from velvet_dawn.models.game_setup import GameSetup


@dataclasses.dataclass
class TurnData:

    turn: int
    turn_start: float
    turn_seconds: int
    active_turn: int

    def json(self):
        return {
            "team": self.active_turn,
            "number": self.turn,
            "start": self.turn_start,
            "seconds": self.turn_seconds,
        }


@dataclasses.dataclass
class GameState:

    phase: int
    players: List[Player]
    teams: List[Team]
    setup: GameSetup
    spawn_area: List[SpawnArea]
    entities: List[Entity]
    turn: TurnData

    def json(self):
        return {
            "phase": self.phase,
            "turn": self.turn.json(),
            "players": {player.name: player.json() for player in self.players},
            "teams": [team.json() for team in self.teams],
            "entities": {entity.id: entity.json() for entity in self.entities},
            "setup": self.setup.json(),
            "spawnArea": [tile.json() for tile in self.spawn_area]
        }
