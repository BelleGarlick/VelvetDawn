import dataclasses
from typing import List

from velvet_dawn.dao.models import Player, Team
from velvet_dawn.models.game_setup import GameSetup


@dataclasses.dataclass
class GameState:
    phase: int
    turn: int
    active_turn: int
    players: List[Player]
    teams: List[Team]
    setup: GameSetup

    def json(self):
        return {
            "phase": self.phase,
            "turn": self.turn,
            "activeTurn": self.active_turn,
            "players": {player.name: player.json() for player in self.players},
            "teams": [team.json() for team in self.teams],
            "setup": self.setup.json()
        }
