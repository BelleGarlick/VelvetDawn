import dataclasses
from typing import List, Dict

from dao.models import Player
from dao.models.teams import Team


@dataclasses.dataclass
class GameState:
    phase: int
    turn: int
    active_turn: int
    players: List[Player]
    teams: List[Team]

    def json(self):
        return {
            "phase": self.phase,
            "turn": self.turn,
            "activeTurn": self.active_turn,
            "players": {player.name: player.json() for player in self.players},
            "teams": [team.json() for team in self.teams]
        }
