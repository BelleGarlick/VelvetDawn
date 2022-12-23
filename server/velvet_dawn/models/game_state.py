import dataclasses
from typing import List

from velvet_dawn.dao.models import Player, Team, SpawnArea, Entity
from velvet_dawn.models.game_setup import GameSetup


@dataclasses.dataclass
class GameState:

    phase: int
    turn: int
    active_turn: int
    players: List[Player]
    teams: List[Team]
    setup: GameSetup
    spawn_area: List[SpawnArea]
    entities: List[Entity]

    def json(self):
        return {
            "phase": self.phase,
            "turn": self.turn,
            "activeTurn": self.active_turn,
            "players": {player.name: player.json() for player in self.players},
            "teams": [team.json() for team in self.teams],
            "entities": {entity.id: entity.json() for entity in self.entities},
            "setup": self.setup.json(),
            "spawnArea": [tile.json() for tile in self.spawn_area]
        }
